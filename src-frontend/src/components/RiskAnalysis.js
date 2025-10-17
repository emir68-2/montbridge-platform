import React from 'react';
import { Card, Row, Col, Typography, List, Tag, Alert, Progress, Statistic, Space, Divider } from 'antd';
import { 
  AlertOutlined, 
  WarningOutlined, 
  InfoCircleOutlined, 
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  UserOutlined,
  BankOutlined
} from '@ant-design/icons';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const { Title, Text } = Typography;

function RiskAnalysis({ analysisData }) {
  if (!analysisData) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Alert
          message="No Risk Analysis Data Available"
          description="Please run the complete analysis to view risk assessment details."
          type="info"
          showIcon
        />
      </div>
    );
  }

  const { risk_summary, recommendations } = analysisData;

  const getRiskColor = (severity) => {
    switch (severity) {
      case 'high': return '#ff4d4f';
      case 'medium': return '#faad14';
      case 'low': return '#52c41a';
      default: return '#d9d9d9';
    }
  };

  const getRiskIcon = (severity) => {
    switch (severity) {
      case 'high': return <AlertOutlined />;
      case 'medium': return <WarningOutlined />;
      case 'low': return <InfoCircleOutlined />;
      default: return <InfoCircleOutlined />;
    }
  };

  // Prepare data for risk distribution chart
  const riskDistributionData = [
    { name: 'High', value: risk_summary?.high_risk_count || 0, color: '#ff4d4f' },
    { name: 'Medium', value: risk_summary?.medium_risk_count || 0, color: '#faad14' },
    { name: 'Low', value: risk_summary?.low_risk_count || 0, color: '#52c41a' },
  ];

  const COLORS = ['#ff4d4f', '#faad14', '#52c41a'];

  // Risk categories data
  const riskCategories = [
    { name: 'Financial', count: 3, color: '#1890ff' },
    { name: 'Operational', count: 2, color: '#52c41a' },
    { name: 'Market', count: 1, color: '#faad14' },
    { name: 'Regulatory', count: 1, color: '#ff4d4f' },
    { name: 'Management', count: 0, color: '#722ed1' },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>Risk Analysis & Due Diligence</Title>
      
      {/* Risk Overview Cards */}
      <Row gutter={24} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="Total Risk Factors"
              value={risk_summary?.total_risks || 0}
              prefix={<ExclamationCircleOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="High Risk Count"
              value={risk_summary?.high_risk_count || 0}
              valueStyle={{ color: '#ff4d4f' }}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="Medium Risk Count"
              value={risk_summary?.medium_risk_count || 0}
              valueStyle={{ color: '#faad14' }}
              prefix={<WarningOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="Risk Score"
              value={risk_summary?.risk_score || 0}
              suffix="/100"
              valueStyle={{ color: risk_summary?.risk_score > 70 ? '#ff4d4f' : risk_summary?.risk_score > 40 ? '#faad14' : '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Risk Distribution Charts */}
      <Row gutter={24} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="Risk Distribution" className="dashboard-card">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={riskDistributionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {riskDistributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        
        <Col span={12}>
          <Card title="Risk Categories" className="dashboard-card">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={riskCategories}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#1890ff" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      {/* Detailed Risk Breakdown */}
      <Row gutter={24}>
        {['high', 'medium', 'low'].map(severity => {
          const risks = risk_summary?.[`${severity}_risks`] || [];
          return (
            <Col span={8} key={severity}>
              <Card 
                title={
                  <Space>
                    {getRiskIcon(severity)}
                    <span style={{ color: getRiskColor(severity) }}>
                      {severity.toUpperCase()} RISKS
                    </span>
                    <Tag color={getRiskColor(severity)}>{risks.length}</Tag>
                  </Space>
                }
                className="dashboard-card"
              >
                {risks.length > 0 ? (
                  <List
                    size="small"
                    dataSource={risks}
                    renderItem={(risk, index) => (
                      <List.Item>
                        <List.Item.Meta
                          title={
                            <Space>
                              <Tag color={getRiskColor(severity)} size="small">
                                {risk.type || 'General'}
                              </Tag>
                              <Text style={{ fontSize: '12px' }}>
                                {risk.source || 'Analysis'}
                              </Text>
                            </Space>
                          }
                          description={
                            <Text style={{ fontSize: '12px' }}>
                              {risk.description?.length > 100 
                                ? `${risk.description.substring(0, 100)}...` 
                                : risk.description
                              }
                            </Text>
                          }
                        />
                      </List.Item>
                    )}
                  />
                ) : (
                  <div style={{ textAlign: 'center', padding: '20px' }}>
                    <CheckCircleOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
                    <div style={{ marginTop: '8px' }}>
                      <Text type="secondary">No {severity} risks identified</Text>
                    </div>
                  </div>
                )}
              </Card>
            </Col>
          );
        })}
      </Row>

      {/* Risk Mitigation Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <Card title="Risk Mitigation Recommendations" className="dashboard-card" style={{ marginTop: 24 }}>
          <List
            dataSource={recommendations}
            renderItem={(recommendation) => (
              <List.Item>
                <Card size="small" style={{ width: '100%' }}>
                  <Title level={5}>
                    <Space>
                      <DollarOutlined />
                      {recommendation.category}
                    </Space>
                  </Title>
                  <List
                    size="small"
                    dataSource={recommendation.recommendations}
                    renderItem={(rec) => (
                      <List.Item>
                        <Space>
                          <CheckCircleOutlined style={{ color: '#52c41a' }} />
                          <Text>{rec}</Text>
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </List.Item>
            )}
          />
        </Card>
      )}

      {/* Risk Assessment Summary */}
      <Card title="Risk Assessment Summary" className="dashboard-card" style={{ marginTop: 24 }}>
        <Row gutter={24}>
          <Col span={12}>
            <Alert
              message="Overall Risk Assessment"
              description={
                <div>
                  <p>
                    The target company presents a{' '}
                    <strong style={{ 
                      color: risk_summary?.risk_score > 70 ? '#ff4d4f' : 
                             risk_summary?.risk_score > 40 ? '#faad14' : '#52c41a'
                    }}>
                      {risk_summary?.risk_score > 70 ? 'HIGH' : 
                       risk_summary?.risk_score > 40 ? 'MODERATE' : 'LOW'}
                    </strong>{' '}
                    risk profile with {risk_summary?.total_risks || 0} identified risk factors.
                  </p>
                  <p>
                    {risk_summary?.high_risk_count > 0 && (
                      <>
                        <strong>{risk_summary.high_risk_count}</strong> high-severity risks require immediate attention.
                        <br />
                      </>
                    )}
                    {risk_summary?.medium_risk_count > 0 && (
                      <>
                        <strong>{risk_summary.medium_risk_count}</strong> medium-severity risks should be addressed in due diligence.
                        <br />
                      </>
                    )}
                    {risk_summary?.low_risk_count > 0 && (
                      <>
                        <strong>{risk_summary.low_risk_count}</strong> low-severity risks should be monitored post-acquisition.
                      </>
                    )}
                  </p>
                </div>
              }
              type={risk_summary?.risk_score > 70 ? 'error' : 
                    risk_summary?.risk_score > 40 ? 'warning' : 'info'}
              showIcon
            />
          </Col>
          
          <Col span={12}>
            <div style={{ padding: '16px' }}>
              <Title level={5}>Risk Score Breakdown</Title>
              <Progress 
                percent={risk_summary?.risk_score || 0} 
                status={risk_summary?.risk_score > 70 ? 'exception' : 
                        risk_summary?.risk_score > 40 ? 'normal' : 'success'}
                strokeColor={{
                  '0%': '#52c41a',
                  '50%': '#faad14',
                  '100%': '#ff4d4f',
                }}
              />
              <div style={{ marginTop: '16px', fontSize: '12px', color: '#666' }}>
                <p>• 0-30: Low Risk - Proceed with standard due diligence</p>
                <p>• 31-70: Moderate Risk - Enhanced due diligence recommended</p>
                <p>• 71-100: High Risk - Extensive due diligence required</p>
              </div>
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
}

export default RiskAnalysis;
