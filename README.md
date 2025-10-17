# Private Equity Due Diligence Platform

A comprehensive web-based platform designed to assist private equity firms in evaluating small and medium-sized businesses for potential acquisition. The platform processes both structured and unstructured data, generates financial models and valuations, and conducts operational due diligence with risk analysis.

## Features

### 1. Data Ingestion & Processing
- **Structured Data**: Accepts Excel, CSV files containing financial statements
- **Unstructured Data**: Processes PDFs, Word documents, and text files
- **NLP Extraction**: Uses AI techniques to extract key information from documents
- **Data Validation**: Identifies inconsistencies between different data sources

### 2. Financial Modelling & Valuation
- **DCF Analysis**: Discounted Cash Flow valuation with 5-year projections
- **Comparable Company Analysis**: Valuation based on industry multiples
- **Precedent Transactions**: Analysis based on similar acquisition transactions
- **Sensitivity Analysis**: Tests impact of changes in key variables
- **Valuation Dashboard**: Clear visualization of valuation ranges and assumptions

### 3. Operational Due Diligence & Risk Analysis
- **Inconsistency Detection**: Identifies discrepancies between data sources
- **Risk Categorization**: Classifies risks as High, Medium, or Low severity
- **AI-Driven Insights**: Detects contradictory narratives and potential issues
- **Risk Mitigation Recommendations**: Suggests negotiation points and deal structures
- **Risk Dashboard**: Comprehensive risk assessment with visual indicators

### 4. User Experience
- **Modern Web Interface**: Built with React and Ant Design
- **Intuitive Navigation**: Clear dashboard with organized sections
- **Real-time Processing**: Live updates during file processing and analysis
- **Responsive Design**: Works on desktop and tablet devices

## Technology Stack

### Backend
- **Python Flask**: RESTful API server
- **Pandas & NumPy**: Data processing and analysis
- **spaCy & Transformers**: Natural Language Processing
- **PyPDF2 & python-docx**: Document processing

### Frontend
- **React 18**: Modern UI framework
- **Ant Design**: Professional UI components
- **Recharts**: Data visualization
- **Axios**: HTTP client for API communication

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Create uploads directory:**
   ```bash
   mkdir uploads
   ```

4. **Run the Flask server:**
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd src-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Usage

### 1. Upload Files
- Navigate to the "Upload Files" section
- Upload financial statements (CSV, Excel) and documents (PDF, Word, TXT)
- Click "Run Complete Analysis" to process all files

### 2. View Dashboard
- The dashboard provides an overview of:
  - Valuation summary with multiple methods
  - Risk analysis with severity levels
  - Key highlights and recommendations
  - Interactive charts and visualizations

### 3. Detailed Analysis
- **Valuation**: View detailed DCF, comparable analysis, and sensitivity analysis
- **Risk Analysis**: Examine specific risk factors and mitigation recommendations

## Sample Data

The platform includes sample data in the `sample_data/` directory:
- `sample_financials.csv`: Example financial statements
- `sample_investment_memo.txt`: Sample investment memorandum

## API Endpoints

### Core Endpoints
- `POST /api/upload`: Upload files for processing
- `POST /api/process`: Process uploaded files and extract information
- `POST /api/valuation`: Generate financial models and valuations
- `POST /api/risk-analysis`: Conduct risk analysis and due diligence
- `POST /api/dashboard`: Get comprehensive dashboard data

### Utility Endpoints
- `GET /api/health`: Health check endpoint

## Methodology

### Valuation Methods

1. **Discounted Cash Flow (DCF)**
   - 5-year cash flow projections
   - Terminal value calculation
   - Weighted Average Cost of Capital (WACC) discounting
   - Default assumptions: 2.5% terminal growth, 12% discount rate

2. **Comparable Company Analysis**
   - Industry multiples (EV/Revenue, EV/EBITDA, P/E)
   - Market-based valuation approach
   - Adjustments for size and growth differences

3. **Precedent Transactions**
   - Historical acquisition multiples
   - Control premium considerations
   - Similar transaction analysis

### Risk Analysis Framework

1. **Financial Risks**
   - Debt levels and leverage ratios
   - Cash flow sustainability
   - Revenue concentration

2. **Operational Risks**
   - Management quality and experience
   - Operational efficiency
   - Supply chain dependencies

3. **Market Risks**
   - Competitive positioning
   - Market growth prospects
   - Customer concentration

4. **Regulatory Risks**
   - Compliance requirements
   - Legal issues
   - Regulatory changes

## Future Enhancements

- **Advanced NLP**: Integration with GPT models for better document analysis
- **Market Data Integration**: Real-time industry multiples and benchmarks
- **Collaborative Features**: Multi-user access and commenting
- **Report Generation**: Automated PDF report generation
- **API Integration**: Connect with external data sources and CRMs

## Contributing

This is a university project prototype. For production use, additional security measures, error handling, and scalability improvements would be required.

## License

This project is created for educational purposes as part of a university assignment.
# montbridge-platform
