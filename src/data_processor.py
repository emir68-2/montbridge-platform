import pandas as pd
import PyPDF2
import docx
import os
from typing import Dict, Any, List
import logging
import re

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    
try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False

class DataProcessor:
    """Handles processing of both structured and unstructured data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_structured_file(self, file_path: str) -> pd.DataFrame:
        """Process structured data files (CSV, Excel)"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported structured file format: {file_path}")
            
            # Clean and standardize the data
            df = self._clean_structured_data(df)
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing structured file {file_path}: {str(e)}")
            raise
    
    def process_unstructured_file(self, file_path: str) -> str:
        """Process unstructured data files (PDF, DOCX, TXT)"""
        try:
            if file_path.endswith('.pdf'):
                return self._extract_pdf_text(file_path)
            elif file_path.endswith('.docx'):
                return self._extract_docx_text(file_path)
            elif file_path.endswith('.txt'):
                return self._extract_txt_text(file_path)
            else:
                raise ValueError(f"Unsupported unstructured file format: {file_path}")
                
        except Exception as e:
            self.logger.error(f"Error processing unstructured file {file_path}: {str(e)}")
            raise
    
    def _clean_structured_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize structured data"""
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Convert numeric columns
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='ignore')
        
        return df
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF files with enhanced table detection"""
        text = ""
        
        # Try advanced PDF extraction with pdfplumber (better for tables)
        if PDFPLUMBER_AVAILABLE:
            try:
                text = self._extract_pdf_with_pdfplumber(file_path)
                if text and len(text.strip()) > 100:  # If we got good content
                    return text
            except Exception as e:
                self.logger.warning(f"pdfplumber extraction failed, falling back to PyPDF2: {str(e)}")
        
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            self.logger.error(f"PyPDF2 extraction failed: {str(e)}")
            
        return text
    
    def _extract_pdf_with_pdfplumber(self, file_path: str) -> str:
        """Extract text and tables from PDF using pdfplumber (better for financial statements)"""
        text = ""
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract regular text
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text + "\n"
                
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    for table_num, table in enumerate(tables):
                        text += f"\n[Table {table_num + 1}]\n"
                        # Convert table to readable format
                        for row in table:
                            if row:  # Skip empty rows
                                row_text = " | ".join([str(cell) if cell else "" for cell in row])
                                text += row_text + "\n"
                        text += "\n"
        
        return text
    
    def extract_pdf_tables_to_dataframes(self, file_path: str) -> List[pd.DataFrame]:
        """Extract tables from PDF as pandas DataFrames (for financial statements)"""
        dataframes = []
        
        # Try tabula-py first (excellent for table extraction)
        if TABULA_AVAILABLE:
            try:
                # Extract all tables from PDF
                tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
                for df in tables:
                    if not df.empty and len(df) > 0:
                        dataframes.append(df)
                
                if dataframes:
                    self.logger.info(f"Extracted {len(dataframes)} tables from PDF using tabula")
                    return dataframes
            except Exception as e:
                self.logger.warning(f"tabula extraction failed: {str(e)}")
        
        # Try pdfplumber as fallback
        if PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        for table in tables:
                            if table and len(table) > 1:  # At least header + 1 row
                                # Convert to DataFrame
                                df = pd.DataFrame(table[1:], columns=table[0])
                                dataframes.append(df)
                
                if dataframes:
                    self.logger.info(f"Extracted {len(dataframes)} tables from PDF using pdfplumber")
            except Exception as e:
                self.logger.warning(f"pdfplumber table extraction failed: {str(e)}")
        
        return dataframes
    
    def extract_financial_data_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract financial data from PDF financial statements"""
        result = {
            'text': '',
            'tables': [],
            'financial_figures': {},
            'extracted_data': []
        }
        
        # Extract text
        result['text'] = self._extract_pdf_text(file_path)
        
        # Extract tables as DataFrames
        result['tables'] = self.extract_pdf_tables_to_dataframes(file_path)
        
        # Parse financial figures from text using regex
        result['financial_figures'] = self._extract_financial_figures_from_text(result['text'])
        
        # Try to identify and structure financial data from tables
        if result['tables']:
            for idx, df in enumerate(result['tables']):
                structured_data = self._identify_financial_data_in_table(df)
                if structured_data:
                    result['extracted_data'].append({
                        'table_index': idx,
                        'data': structured_data
                    })
        
        return result
    
    def _extract_financial_figures_from_text(self, text: str) -> Dict[str, Any]:
        """Extract financial figures from text using pattern matching"""
        figures = {}
        
        # Patterns for common financial metrics
        patterns = {
            'revenue': r'(?:revenue|sales)[\s:]+\$?\s*([\d,\.]+)\s*(?:million|m|k|thousand|billion|b)?',
            'ebitda': r'ebitda[\s:]+\$?\s*([\d,\.]+)\s*(?:million|m|k|thousand|billion|b)?',
            'net_income': r'(?:net income|profit)[\s:]+\$?\s*([\d,\.]+)\s*(?:million|m|k|thousand|billion|b)?',
            'assets': r'(?:total assets)[\s:]+\$?\s*([\d,\.]+)\s*(?:million|m|k|thousand|billion|b)?',
            'liabilities': r'(?:total liabilities)[\s:]+\$?\s*([\d,\.]+)\s*(?:million|m|k|thousand|billion|b)?',
            'cash': r'(?:cash|cash and equivalents)[\s:]+\$?\s*([\d,\.]+)\s*(?:million|m|k|thousand|billion|b)?',
        }
        
        text_lower = text.lower()
        
        for metric, pattern in patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Get the first match and clean it
                value_str = matches[0].replace(',', '')
                try:
                    figures[metric] = float(value_str)
                except ValueError:
                    pass
        
        return figures
    
    def _identify_financial_data_in_table(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify financial statement data in a DataFrame extracted from PDF"""
        if df.empty or len(df) < 2:
            return None
        
        financial_data = {}
        
        # Look for year columns and financial metrics
        for col in df.columns:
            col_str = str(col).lower()
            # Check if column contains years
            if re.match(r'^\d{4}$', str(col).strip()):
                financial_data[col] = {}
        
        # Look for financial metrics in rows
        for idx, row in df.iterrows():
            first_col = str(row.iloc[0]).lower() if len(row) > 0 else ""
            
            # Common financial statement line items
            if any(keyword in first_col for keyword in ['revenue', 'sales', 'income', 'ebitda', 'assets', 'liabilities', 'cash', 'debt']):
                metric_name = first_col.strip()
                
                # Extract values for each year
                for col in df.columns[1:]:  # Skip first column (metric names)
                    value_str = str(row[col])
                    # Try to convert to number
                    value_str = value_str.replace(',', '').replace('$', '').replace('(', '-').replace(')', '').strip()
                    try:
                        value = float(value_str)
                        if col not in financial_data:
                            financial_data[col] = {}
                        financial_data[col][metric_name] = value
                    except ValueError:
                        pass
        
        return financial_data if financial_data else None
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX files"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT files"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def identify_financial_statements(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify different types of financial statements in structured data"""
        financial_statements = {
            "income_statement": None,
            "balance_sheet": None,
            "cash_flow": None,
            "other": []
        }
        
        # Look for common financial statement indicators in column names
        income_keywords = ['revenue', 'sales', 'income', 'profit', 'ebitda', 'net_income']
        balance_keywords = ['assets', 'liabilities', 'equity', 'cash', 'inventory', 'debt']
        cashflow_keywords = ['operating', 'investing', 'financing', 'cash_flow', 'capex']
        
        # Simple keyword matching - in a real implementation, this would be more sophisticated
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in income_keywords):
                financial_statements["income_statement"] = df
            elif any(keyword in col_lower for keyword in balance_keywords):
                financial_statements["balance_sheet"] = df
            elif any(keyword in col_lower for keyword in cashflow_keywords):
                financial_statements["cash_flow"] = df
            else:
                financial_statements["other"].append(col)
        
        return financial_statements
