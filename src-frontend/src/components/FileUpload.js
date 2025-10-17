import React, { useState, useCallback } from 'react';
import { Upload, Button, Card, List, Progress, message, Row, Col, Typography, Space, Divider, Badge, Steps } from 'antd';
import { InboxOutlined, FileTextOutlined, BarChartOutlined, CloudUploadOutlined, FileExcelOutlined, FilePdfOutlined } from '@ant-design/icons';
import { ApiService } from '../services/apiService';

const { Dragger } = Upload;
const { Title, Text } = Typography;

function FileUpload({ onAnalysisComplete }) {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleUpload = useCallback(async (options) => {
    const { file, onSuccess, onError, onProgress } = options;
    
    try {
      setProcessing(true);
      setProgress(0);
      
      // Upload files
      const uploadResponse = await ApiService.uploadFiles([file]);
      
      if (uploadResponse.uploaded_files && uploadResponse.uploaded_files.length > 0) {
        const uploadedFile = uploadResponse.uploaded_files[0];
        setUploadedFiles(prev => [...prev, uploadedFile]);
        
        onSuccess(uploadResponse);
        message.success(`File ${file.name} uploaded successfully`);
      } else {
        onError(new Error('Upload failed'));
        message.error('File upload failed');
      }
    } catch (error) {
      onError(error);
      message.error(`Upload failed: ${error.message}`);
    } finally {
      setProcessing(false);
    }
  }, []);

  const handleAnalysis = async () => {
    if (uploadedFiles.length === 0) {
      message.warning('Please upload files first');
      return;
    }

    try {
      setProcessing(true);
      setProgress(10);

      // Process files
      const filePaths = uploadedFiles.map(file => file.filepath);
      const processResponse = await ApiService.processData(filePaths);
      setProgress(30);

      // Generate valuation
      const financialData = {
        revenue: 1000000, // Default values - in real app, extract from structured data
        ebitda_margin: 0.15,
        growth_rate: 0.08
      };
      const assumptions = {
        terminal_growth_rate: 0.025,
        discount_rate: 0.12,
        tax_rate: 0.25
      };
      
      const valuationResults = await ApiService.generateValuation(financialData, assumptions);
      setProgress(60);

      // Analyze risks
      const riskAnalysis = await ApiService.analyzeRisks(
        processResponse.structured_data,
        processResponse.unstructured_data,
        processResponse.extracted_info
      );
      setProgress(90);

      // Get dashboard data
      const dashboardData = await ApiService.getDashboardData(valuationResults, riskAnalysis);
      setProgress(100);

      setAnalysisResults(dashboardData);
      onAnalysisComplete(dashboardData);
      
      message.success('Analysis completed successfully!');
    } catch (error) {
      message.error(`Analysis failed: ${error.message}`);
    } finally {
      setProcessing(false);
    }
  };

  const removeFile = (filename) => {
    setUploadedFiles(prev => prev.filter(file => file.filename !== filename));
  };

  const uploadProps = {
    name: 'file',
    multiple: true,
    accept: '.pdf,.docx,.xlsx,.csv,.txt',
    customRequest: handleUpload,
    showUploadList: false,
    disabled: processing,
  };

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>Upload Company Documents</Title>
      <Text type="secondary">
        Upload structured financial data (Excel, CSV) and unstructured documents (PDF, Word) for analysis.
      </Text>
      
      <Row gutter={24} style={{ marginTop: 24 }}>
        <Col span={16}>
          <Card title="File Upload" className="dashboard-card">
            <Dragger {...uploadProps}>
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">
                Click or drag files to this area to upload
              </p>
              <p className="ant-upload-hint">
                Support for PDF, DOCX, XLSX, CSV, and TXT files. Maximum file size: 16MB
              </p>
            </Dragger>
            
            {processing && (
              <div style={{ marginTop: 16 }}>
                <Progress percent={progress} status="active" />
                <Text>Processing files and generating analysis...</Text>
              </div>
            )}
          </Card>
        </Col>
        
        <Col span={8}>
          <Card title="Uploaded Files" className="dashboard-card">
            {uploadedFiles.length === 0 ? (
              <Text type="secondary">No files uploaded yet</Text>
            ) : (
              <List
                size="small"
                dataSource={uploadedFiles}
                renderItem={(file) => (
                  <List.Item
                    actions={[
                      <Button 
                        type="link" 
                        danger 
                        size="small"
                        onClick={() => removeFile(file.filename)}
                        disabled={processing}
                      >
                        Remove
                      </Button>
                    ]}
                  >
                    <Space>
                      <FileTextOutlined />
                      <Text>{file.filename}</Text>
                      <Text type="secondary">({file.type})</Text>
                    </Space>
                  </List.Item>
                )}
              />
            )}
            
            <Divider />
            
            <Button
              type="primary"
              size="large"
              onClick={handleAnalysis}
              disabled={uploadedFiles.length === 0 || processing}
              loading={processing}
              block
            >
              <BarChartOutlined />
              Run Complete Analysis
            </Button>
          </Card>
        </Col>
      </Row>
      
      {analysisResults && (
        <Card title="Analysis Results Summary" className="dashboard-card" style={{ marginTop: 24 }}>
          <Row gutter={16}>
            <Col span={8}>
              <div className="valuation-metric">
                <div className="valuation-value">
                  ${analysisResults.valuation_summary?.valuation_range?.low?.toLocaleString() || 'N/A'}
                </div>
                <div className="valuation-label">Low Valuation</div>
              </div>
            </Col>
            <Col span={8}>
              <div className="valuation-metric">
                <div className="valuation-value">
                  ${analysisResults.valuation_summary?.valuation_range?.high?.toLocaleString() || 'N/A'}
                </div>
                <div className="valuation-label">High Valuation</div>
              </div>
            </Col>
            <Col span={8}>
              <div className="valuation-metric">
                <div className="valuation-value">
                  {analysisResults.risk_summary?.total_risks || 0}
                </div>
                <div className="valuation-label">Risk Factors</div>
              </div>
            </Col>
          </Row>
        </Card>
      )}
    </div>
  );
}

export default FileUpload;
