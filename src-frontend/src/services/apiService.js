import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 seconds timeout for file processing
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  async healthCheck() {
    try {
      const response = await this.api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }

  async uploadFiles(files) {
    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await this.api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      throw new Error(`File upload failed: ${error.response?.data?.error || error.message}`);
    }
  }

  async processData(filePaths) {
    try {
      const response = await this.api.post('/process', {
        file_paths: filePaths,
      });

      return response.data;
    } catch (error) {
      throw new Error(`Data processing failed: ${error.response?.data?.error || error.message}`);
    }
  }

  async generateValuation(financialData, assumptions) {
    try {
      const response = await this.api.post('/valuation', {
        financial_data: financialData,
        assumptions: assumptions,
      });

      return response.data;
    } catch (error) {
      throw new Error(`Valuation generation failed: ${error.response?.data?.error || error.message}`);
    }
  }

  async analyzeRisks(structuredData, unstructuredData, extractedInfo) {
    try {
      const response = await this.api.post('/risk-analysis', {
        structured_data: structuredData,
        unstructured_data: unstructuredData,
        extracted_info: extractedInfo,
      });

      return response.data;
    } catch (error) {
      throw new Error(`Risk analysis failed: ${error.response?.data?.error || error.message}`);
    }
  }

  async getDashboardData(valuationResults, riskAnalysis) {
    try {
      const response = await this.api.post('/dashboard', {
        valuation_results: valuationResults,
        risk_analysis: riskAnalysis,
      });

      return response.data;
    } catch (error) {
      throw new Error(`Dashboard data retrieval failed: ${error.response?.data?.error || error.message}`);
    }
  }
}

export const ApiService = new ApiService();
