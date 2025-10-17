# Private Equity Due Diligence Platform - Demo Guide

## Quick Start Demo

This guide will walk you through a complete demonstration of the PE Due Diligence Platform using the provided sample data.

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Terminal/Command Prompt access

### Step 1: Start the Backend Server

1. Open a terminal and navigate to the project directory
2. Make the startup script executable:
   ```bash
   chmod +x start_backend.sh
   ```
3. Run the backend startup script:
   ```bash
   ./start_backend.sh
   ```
   
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   mkdir uploads
   python app.py
   ```

4. Wait for the server to start (you'll see "Running on http://0.0.0.0:5000")

### Step 2: Start the Frontend (New Terminal)

1. Open a new terminal window
2. Navigate to the project directory
3. Make the frontend startup script executable:
   ```bash
   chmod +x start_frontend.sh
   ```
4. Run the frontend startup script:
   ```bash
   ./start_frontend.sh
   ```
   
   Or manually:
   ```bash
   cd src-frontend
   npm install
   npm start
   ```

5. The browser should automatically open to http://localhost:3000

### Step 3: Demo Walkthrough

#### 3.1 Upload Sample Files
1. Click on "Upload Files" in the navigation menu
2. Upload the sample files:
   - `sample_data/sample_financials.csv` (structured financial data)
   - `sample_data/sample_investment_memo.txt` (unstructured document)
3. Click "Run Complete Analysis"

#### 3.2 View Dashboard Results
1. After processing completes, you'll be redirected to the dashboard
2. Observe the key highlights and valuation summary
3. Review the risk analysis with color-coded severity levels
4. Examine the interactive charts showing valuation methods and risk distribution

#### 3.3 Explore Detailed Valuation
1. Click on "Valuation" in the navigation
2. Review the three valuation methods:
   - DCF (Discounted Cash Flow)
   - Comparable Company Analysis
   - Precedent Transactions
3. Examine the sensitivity analysis showing different scenarios
4. View the key assumptions used in the models

#### 3.4 Analyze Risk Factors
1. Click on "Risk Analysis" in the navigation
2. Review the risk breakdown by severity (High, Medium, Low)
3. Examine specific risk factors identified from the documents
4. Read the risk mitigation recommendations
5. View the overall risk assessment and score

## Sample Data Analysis

### Technology Solutions Inc. - Sample Company

The platform will analyze the following sample data:

**Financial Metrics (from sample_financials.csv):**
- Revenue: $1.22M (2023)
- Growth Rate: 15% annually
- EBITDA Margin: 15%
- Debt-to-Equity: ~0.4

**Key Information (from sample_investment_memo.txt):**
- Software company specializing in enterprise automation
- Strong management team
- Growing customer base (75 clients)
- Some customer concentration risk (top 3 customers = 60% revenue)

### Expected Results

**Valuation Range:** Approximately $800K - $1.6M
- DCF Method: Based on projected cash flows
- Comparable Analysis: Industry multiple-based
- Precedent Transactions: Historical acquisition multiples

**Risk Factors Identified:**
- High: Customer concentration (top 3 customers = 60% revenue)
- Medium: Competitive market pressure
- Low: Regulatory compliance considerations

**Recommendations:**
- Price adjustment for customer concentration risk
- Enhanced due diligence on customer contracts
- Warranty requirements for key customer relationships

## Key Features Demonstrated

1. **Data Processing**: Automatic extraction of financial metrics and key information
2. **Valuation Models**: Three different valuation approaches with sensitivity analysis
3. **Risk Analysis**: AI-powered risk identification and categorization
4. **Visualization**: Interactive charts and clear dashboard presentation
5. **Recommendations**: Practical suggestions for deal structuring and negotiation

## Troubleshooting

### Backend Issues
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify spaCy model is downloaded: `python -m spacy download en_core_web_sm`
- Check that port 5000 is available

### Frontend Issues
- Ensure Node.js 16+ is installed
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that port 3000 is available

### Common Issues
- **CORS Errors**: Ensure backend is running on port 5000
- **File Upload Errors**: Check file size limits (16MB max)
- **Processing Errors**: Verify uploaded files are in supported formats

## Next Steps for Production

This is a prototype demonstration. For production use, consider:

1. **Security**: Implement authentication and authorization
2. **Scalability**: Add database storage and caching
3. **Enhanced NLP**: Integrate with GPT models for better document analysis
4. **Market Data**: Connect to real-time industry multiples
5. **Reporting**: Generate PDF reports for stakeholders
6. **Collaboration**: Multi-user access and commenting features

## Support

For questions or issues with this demo:
1. Check the README.md for detailed setup instructions
2. Review the API endpoints in app.py
3. Examine the component structure in src-frontend/src/components/
4. Verify sample data format in sample_data/ directory
