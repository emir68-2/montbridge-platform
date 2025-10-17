import React, { useState, useEffect } from 'react';
import { Layout, Menu, Card, Row, Col, Typography, Button, message, Spin, ConfigProvider, theme } from 'antd';
import { UploadOutlined, BarChartOutlined, AlertOutlined, FileTextOutlined, HomeOutlined, SettingOutlined } from '@ant-design/icons';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';

import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import Valuation from './components/Valuation';
import RiskAnalysis from './components/RiskAnalysis';
import { ApiService } from './services/apiService';

const { Header, Content, Sider } = Layout;
const { Title } = Typography;

function AppContent() {
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/upload',
      icon: <UploadOutlined />,
      label: 'Upload & Process',
    },
    {
      key: '/valuation',
      icon: <BarChartOutlined />,
      label: 'Valuation Analysis',
    },
    {
      key: '/risks',
      icon: <AlertOutlined />,
      label: 'Risk Assessment',
    },
  ];

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    message.success('Analysis completed successfully!');
    navigate('/');
  };

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#1890ff',
          colorSuccess: '#52c41a',
          colorWarning: '#faad14',
          colorError: '#ff4d4f',
          colorInfo: '#1890ff',
          borderRadius: 8,
          wireframe: false,
        },
      }}
    >
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          background: 'linear-gradient(135deg, #001529 0%, #1890ff 100%)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          padding: '0 24px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ 
              width: 40, 
              height: 40, 
              background: 'rgba(255,255,255,0.2)', 
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginRight: 16
            }}>
              <BarChartOutlined style={{ color: 'white', fontSize: '20px' }} />
            </div>
            <Title level={3} style={{ color: 'white', margin: 0 }}>
              PE Due Diligence Platform
            </Title>
          </div>
          <div style={{ color: 'rgba(255,255,255,0.85)', fontSize: '14px', fontWeight: 500 }}>
            Professional Investment Analysis
          </div>
        </Header>
        
        <Layout>
          <Sider 
            width={220} 
            style={{ 
              background: '#fff',
              boxShadow: '2px 0 8px rgba(0,0,0,0.06)'
            }}
          >
            <Menu
              mode="inline"
              selectedKeys={[location.pathname]}
              style={{ 
                height: '100%', 
                borderRight: 0,
                padding: '16px 0'
              }}
              items={menuItems}
              onClick={({ key }) => navigate(key)}
            />
          </Sider>
          
          <Layout style={{ background: '#f5f5f5' }}>
            <Content style={{ 
              margin: 0, 
              minHeight: 280,
              padding: '24px',
              background: '#f5f5f5'
            }}>
              {loading && (
                <div className="loading-spinner">
                  <Spin size="large" />
                </div>
              )}
              
              <Routes>
                <Route 
                  path="/" 
                  element={<Dashboard analysisData={analysisData} />} 
                />
                <Route 
                  path="/upload" 
                  element={<FileUpload onAnalysisComplete={handleAnalysisComplete} />} 
                />
                <Route 
                  path="/valuation" 
                  element={<Valuation analysisData={analysisData} />} 
                />
                <Route 
                  path="/risks" 
                  element={<RiskAnalysis analysisData={analysisData} />} 
                />
              </Routes>
            </Content>
          </Layout>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
