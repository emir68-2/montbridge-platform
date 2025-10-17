from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import logging

# Import our custom modules
from src.data_processor import DataProcessor
from src.financial_model import FinancialModel
from src.risk_analyzer import RiskAnalyzer
# from src.nlp_extractor import NLPExtractor

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'csv', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize our processing modules
data_processor = DataProcessor()
financial_model = FinancialModel()
risk_analyzer = RiskAnalyzer()
# nlp_extractor = NLPExtractor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads for both structured and unstructured data"""
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    errors = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            uploaded_files.append({
                "filename": filename,
                "filepath": filepath,
                "type": "structured" if filename.endswith(('.xlsx', '.csv')) else "unstructured"
            })
        else:
            errors.append(f"File {file.filename} has invalid format")
    
    return jsonify({
        "uploaded_files": uploaded_files,
        "errors": errors,
        "message": f"Successfully uploaded {len(uploaded_files)} files"
    })

@app.route('/api/process', methods=['POST'])
def process_data():
    """Process uploaded files and extract relevant information"""
    try:
        data = request.get_json()
        file_paths = data.get('file_paths', [])
        
        results = {
            "structured_data": {},
            "unstructured_data": {},
            "extracted_info": {},
            "processing_errors": []
        }
        
        for file_path in file_paths:
            try:
                if file_path.endswith(('.xlsx', '.csv')):
                    # Process structured data
                    df = data_processor.process_structured_file(file_path)
                    results["structured_data"][file_path] = df.to_dict('records')
                    
                elif file_path.endswith(('.pdf', '.docx', '.txt')):
                    # Process unstructured data
                    extracted_text = data_processor.process_unstructured_file(file_path)
                    # nlp_results = nlp_extractor.extract_key_information(extracted_text)
                    results["unstructured_data"][file_path] = extracted_text
                    results["extracted_info"][file_path] = {"text": extracted_text[:500]}
                    
            except Exception as e:
                results["processing_errors"].append(f"Error processing {file_path}: {str(e)}")
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/valuation', methods=['POST'])
def generate_valuation():
    """Generate financial model and valuation"""
    try:
        data = request.get_json()
        financial_data = data.get('financial_data', {})
        assumptions = data.get('assumptions', {})
        
        # Generate valuation using different methods
        dcf_valuation = financial_model.dcf_valuation(financial_data, assumptions)
        comps_valuation = financial_model.comparable_analysis(financial_data, assumptions)
        precedent_valuation = financial_model.precedent_transactions(financial_data, assumptions)
        
        # Calculate sensitivity analysis
        sensitivity = financial_model.sensitivity_analysis(financial_data, assumptions)
        
        results = {
            "dcf_valuation": dcf_valuation,
            "comparable_analysis": comps_valuation,
            "precedent_transactions": precedent_valuation,
            "sensitivity_analysis": sensitivity,
            "valuation_range": {
                "low": min(dcf_valuation.get('value', 0), comps_valuation.get('value', 0), precedent_valuation.get('value', 0)),
                "high": max(dcf_valuation.get('value', 0), comps_valuation.get('value', 0), precedent_valuation.get('value', 0))
            }
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/risk-analysis', methods=['POST'])
def analyze_risks():
    """Conduct operational due diligence and risk analysis"""
    try:
        data = request.get_json()
        structured_data = data.get('structured_data', {})
        unstructured_data = data.get('unstructured_data', {})
        extracted_info = data.get('extracted_info', {})
        
        # Analyze for inconsistencies and risks
        risk_analysis = risk_analyzer.analyze_risks(
            structured_data, unstructured_data, extracted_info
        )
        
        return jsonify(risk_analysis)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard', methods=['POST'])
def get_dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        data = request.get_json()
        
        # Get all analysis results
        valuation_results = data.get('valuation_results', {})
        risk_analysis = data.get('risk_analysis', {})
        
        dashboard_data = {
            "valuation_summary": {
                "dcf_value": valuation_results.get('dcf_valuation', {}).get('value', 0),
                "comparable_value": valuation_results.get('comparable_analysis', {}).get('value', 0),
                "precedent_value": valuation_results.get('precedent_transactions', {}).get('value', 0),
                "valuation_range": valuation_results.get('valuation_range', {})
            },
            "risk_summary": {
                "high_risks": risk_analysis.get('high_risks', []),
                "medium_risks": risk_analysis.get('medium_risks', []),
                "low_risks": risk_analysis.get('low_risks', []),
                "total_risks": len(risk_analysis.get('high_risks', []) + 
                                 risk_analysis.get('medium_risks', []) + 
                                 risk_analysis.get('low_risks', []))
            },
            "recommendations": risk_analysis.get('recommendations', []),
            "key_highlights": risk_analysis.get('key_highlights', [])
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
