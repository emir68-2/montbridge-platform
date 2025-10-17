import pandas as pd
import PyPDF2
import docx
import os
from typing import Dict, Any, List
import logging

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
        """Extract text from PDF files"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
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
