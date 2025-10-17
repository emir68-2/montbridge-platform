import React from 'react';
import { Card, Row, Col, Typography, Statistic, List, Tag, Progress, Alert, Space, Divider, Badge, Avatar } from 'antd';
import { 
  DollarOutlined, 
  TrendingUpOutlined, 
  AlertOutlined, 
  CheckCircleOutlined,
  WarningOutlined,
  InfoCircleOutlined,
  TrophyOutlined,
  RiseOutlined,
  FallOutlined
} from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Area, AreaChart } from 'recharts';

const { Title, Text } = Typography;

function Dashboard({ analysisData }) {
  if (!analysisData) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Alert
          message="No Analysis Data Available"
          description="Please upload files and run analysis to view the dashboard."
          type="info"
          showIcon
        />
      </div>
    );
  }

  const { valuation_summary, risk_summary, recommendations, key_highlights } = analysisData;

  // Prepare data for charts
  const valuationData = [
    { name: 'DCF', value: valuation_summary?.dcf_value || 0 },
    { name: 'Comparable', value: valuation_summary?.comparable_value || 0 },
    { name: 'Precedent', value: valuation_summary?.precedent_value || 0 },
  ];

  const riskData = [
    { name: 'High', value: risk_summary?.high_risk_count || 0, color: '#ff4d4f' },
    { name: 'Medium', value: risk_summary?.medium_risk_count || 0, color: '#faad14' },
    { name: 'Low', value: risk_summary?.low_risk_count || 0, color: '#52c41a' },
  ];

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

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <Title level={2} style={{ margin: 0, color: '#001529' }}>
          📊 Investment Analysis Dashboard
        </Title>
        <Text type="secondary" style={{ fontSize: '16px' }}>
          Comprehensive due diligence insights for Technology Solutions Inc.
        </Text>
      </div>
      
      {/* Key Highlights */}
      {key_highlights && key_highlights.length > 0 && (
        <Card title="Key Highlights" className="dashboard-card" style={{ marginBottom: 24 }}>
          <List
            dataSource={key_highlights}
            renderItem={(highlight) => (
              <List.Item>
                <Space>
                  <CheckCircleOutlined style={{ color: '#52c41a' }} />
                  <Text>{highlight}</Text>
                </Space>
              </List.Item>
            )}
          />
        </Card>
      )}

      <Row gutter={24}>
        {/* Valuation Summary */}
        <Col span={12}>
          <Card title="Valuation Summary" className="dashboard-card">
            <Row gutter={16}>
              <Col span={8}>
                <Statistic
                  title="DCF Valuation"
                  value={valuation_summary?.dcf_value || 0}
                  prefix="$"
                  valueStyle={{ color: '#1890ff' }}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="Comparable Analysis"
                  value={valuation_summary?.comparable_value || 0}
                  prefix="$"
                  valueStyle={{ color: '#1890ff' }}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="Precedent Transactions"
                  value={valuation_summary?.precedent_value || 0}
                  prefix="$"
                  valueStyle={{ color: '#1890ff' }}
                />
              </Col>
            </Row>
            
            <Divider />
            
            <Row gutter={16}>
              <Col span={12}>
                <Statistic
                  title="Valuation Range (Low)"
                  value={valuation_summary?.valuation_range?.low || 0}
                  prefix="$"
                  valueStyle={{ color: '#52c41a' }}
                />
              </Col>
              <Col span={12}>
                <Statistic
                  title="Valuation Range (High)"
                  value={valuation_summary?.valuation_range?.high || 0}
                  prefix="$"
                  valueStyle={{ color: '#faad14' }}
                />
              </Col>
            </Row>
          </Card>
        </Col>

        {/* Risk Summary */}
        <Col span={12}>
          <Card title="Risk Analysis Summary" className="dashboard-card">
            <Row gutter={16}>
              <Col span={8}>
                <Statistic
                  title="High Risks"
                  value={risk_summary?.high_risk_count || 0}
                  valueStyle={{ color: '#ff4d4f' }}
                  prefix={<AlertOutlined />}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="Medium Risks"
                  value={risk_summary?.medium_risk_count || 0}
                  valueStyle={{ color: '#faad14' }}
                  prefix={<WarningOutlined />}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="Low Risks"
                  value={risk_summary?.low_risk_count || 0}
                  valueStyle={{ color: '#52c41a' }}
                  prefix={<InfoCircleOutlined />}
                />
              </Col>
            </Row>
            
            <Divider />
            
            <div style={{ marginTop: 16 }}>
              <Text strong>Overall Risk Score: </Text>
              <Progress 
                percent={risk_summary?.risk_score || 0} 
                status={risk_summary?.risk_score > 70 ? 'exception' : risk_summary?.risk_score > 40 ? 'normal' : 'success'}
                size="small"
              />
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={24} style={{ marginTop: 24 }}>
        {/* Valuation Comparison Chart */}
        <Col span={12}>
          <Card title="Valuation Methods Comparison" className="dashboard-card">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={valuationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Value']} />
                <Bar dataKey="value" fill="#1890ff" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        {/* Risk Distribution Chart */}
        <Col span={12}>
          <Card title="Risk Distribution" className="dashboard-card">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={riskData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#1890ff" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      {/* Top Risks */}
      <Row gutter={24} style={{ marginTop: 24 }}>
        <Col span={24}>
          <Card title="Top Risk Factors" className="dashboard-card">
            <Row gutter={24}>
              {['high', 'medium', 'low'].map(severity => {
                const risks = risk_summary?.[`${severity}_risks`] || [];
                return (
                  <Col span={8} key={severity}>
                    <Title level={5} style={{ color: getRiskColor(severity) }}>
                      {getRiskIcon(severity)} {severity.toUpperCase()} RISKS ({risks.length})
                    </Title>
                    {risks.length > 0 ? (
                      <List
                        size="small"
                        dataSource={risks.slice(0, 3)} // Show top 3
                        renderItem={(risk) => (
                          <List.Item>
                            <Tag color={getRiskColor(severity)} style={{ marginBottom: 4 }}>
                              {risk.type}
                            </Tag>
                            <Text style={{ fontSize: '12px' }}>{risk.description}</Text>
                          </List.Item>
                        )}
                      />
                    ) : (
                      <Text type="secondary">No {severity} risks identified</Text>
                    )}
                  </Col>
                );
              })}
            </Row>
          </Card>
        </Col>
      </Row>

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <Card title="Risk Mitigation Recommendations" className="dashboard-card" style={{ marginTop: 24 }}>
          <List
            dataSource={recommendations}
            renderItem={(recommendation) => (
              <List.Item>
                <List.Item.Meta
                  title={recommendation.category}
                  description={
                    <List
                      size="small"
                      dataSource={recommendation.recommendations}
                      renderItem={(rec) => (
                        <List.Item>
                          <Text>• {rec}</Text>
                        </List.Item>
                      )}
                    />
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
}

export default Dashboard;
