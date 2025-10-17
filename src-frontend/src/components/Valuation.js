import React from 'react';
import { Card, Row, Col, Typography, Statistic, Table, Tag, Alert } from 'antd';
import { DollarOutlined, TrendingUpOutlined, CalculatorOutlined } from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

const { Title, Text } = Typography;

function Valuation({ analysisData }) {
  if (!analysisData) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Alert
          message="No Valuation Data Available"
          description="Please run the complete analysis to view valuation details."
          type="info"
          showIcon
        />
      </div>
    );
  }

  const { valuation_summary } = analysisData;

  // Mock sensitivity data - in real app, this would come from the API
  const sensitivityData = [
    { scenario: 'Pessimistic', value: valuation_summary?.valuation_range?.low || 800000, growth: -2, discount: 16 },
    { scenario: 'Base Case', value: (valuation_summary?.dcf_value + valuation_summary?.comparable_value + valuation_summary?.precedent_value) / 3 || 1200000, growth: 8, discount: 12 },
    { scenario: 'Optimistic', value: valuation_summary?.valuation_range?.high || 1600000, growth: 15, discount: 10 },
  ];

  const valuationMethodsData = [
    {
      key: '1',
      method: 'Discounted Cash Flow (DCF)',
      value: valuation_summary?.dcf_value || 0,
      description: 'Present value of projected future cash flows',
      reliability: 'High'
    },
    {
      key: '2',
      method: 'Comparable Company Analysis',
      value: valuation_summary?.comparable_value || 0,
      description: 'Based on trading multiples of similar public companies',
      reliability: 'Medium'
    },
    {
      key: '3',
      method: 'Precedent Transactions',
      value: valuation_summary?.precedent_value || 0,
      description: 'Based on acquisition multiples of similar transactions',
      reliability: 'High'
    },
  ];

  const valuationColumns = [
    {
      title: 'Method',
      dataIndex: 'method',
      key: 'method',
      render: (text) => <Text strong>{text}</Text>
    },
    {
      title: 'Valuation',
      dataIndex: 'value',
      key: 'value',
      render: (value) => <Text style={{ color: '#1890ff', fontWeight: 'bold' }}>${value?.toLocaleString() || 0}</Text>
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Reliability',
      dataIndex: 'reliability',
      key: 'reliability',
      render: (reliability) => (
        <Tag color={reliability === 'High' ? 'green' : reliability === 'Medium' ? 'orange' : 'red'}>
          {reliability}
        </Tag>
      )
    },
  ];

  const sensitivityColumns = [
    {
      title: 'Scenario',
      dataIndex: 'scenario',
      key: 'scenario',
      render: (text) => <Text strong>{text}</Text>
    },
    {
      title: 'Growth Rate',
      dataIndex: 'growth',
      key: 'growth',
      render: (value) => <Text>{value}%</Text>
    },
    {
      title: 'Discount Rate',
      dataIndex: 'discount',
      key: 'discount',
      render: (value) => <Text>{value}%</Text>
    },
    {
      title: 'Valuation',
      dataIndex: 'value',
      key: 'value',
      render: (value) => <Text style={{ color: '#1890ff', fontWeight: 'bold' }}>${value?.toLocaleString() || 0}</Text>
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>Financial Valuation Analysis</Title>
      
      {/* Valuation Summary Cards */}
      <Row gutter={24} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card className="dashboard-card">
            <Statistic
              title="Enterprise Value Range"
              value={valuation_summary?.valuation_range?.low || 0}
              suffix={`- $${(valuation_summary?.valuation_range?.high || 0).toLocaleString()}`}
              prefix="$"
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="dashboard-card">
            <Statistic
              title="Mid-Point Valuation"
              value={((valuation_summary?.valuation_range?.low || 0) + (valuation_summary?.valuation_range?.high || 0)) / 2}
              prefix="$"
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="dashboard-card">
            <Statistic
              title="Valuation Range"
              value={Math.abs((valuation_summary?.valuation_range?.high || 0) - (valuation_summary?.valuation_range?.low || 0))}
              prefix="$"
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Valuation Methods Chart */}
      <Card title="Valuation Methods Comparison" className="dashboard-card" style={{ marginBottom: 24 }}>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={valuationMethodsData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="method" angle={-45} textAnchor="end" height={100} />
            <YAxis />
            <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Valuation']} />
            <Bar dataKey="value" fill="#1890ff" />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      {/* Valuation Methods Table */}
      <Card title="Valuation Methods Details" className="dashboard-card" style={{ marginBottom: 24 }}>
        <Table
          columns={valuationColumns}
          dataSource={valuationMethodsData}
          pagination={false}
          size="small"
        />
      </Card>

      {/* Sensitivity Analysis */}
      <Row gutter={24}>
        <Col span={12}>
          <Card title="Sensitivity Analysis" className="dashboard-card">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={sensitivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="scenario" />
                <YAxis />
                <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Valuation']} />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#1890ff" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        
        <Col span={12}>
          <Card title="Sensitivity Scenarios" className="dashboard-card">
            <Table
              columns={sensitivityColumns}
              dataSource={sensitivityData}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>

      {/* Key Assumptions */}
      <Card title="Key Valuation Assumptions" className="dashboard-card" style={{ marginTop: 24 }}>
        <Row gutter={24}>
          <Col span={8}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Title level={4} style={{ color: '#1890ff' }}>2.5%</Title>
              <Text>Terminal Growth Rate</Text>
            </div>
          </Col>
          <Col span={8}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Title level={4} style={{ color: '#1890ff' }}>12%</Title>
              <Text>Discount Rate (WACC)</Text>
            </div>
          </Col>
          <Col span={8}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Title level={4} style={{ color: '#1890ff' }}>5 Years</Title>
              <Text>Projection Period</Text>
            </div>
          </Col>
        </Row>
        
        <Row gutter={24}>
          <Col span={8}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Title level={4} style={{ color: '#1890ff' }}>25%</Title>
              <Text>Tax Rate</Text>
            </div>
          </Col>
          <Col span={8}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Title level={4} style={{ color: '#1890ff' }}>3%</Title>
              <Text>CapEx as % of Revenue</Text>
            </div>
          </Col>
          <Col span={8}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Title level={4} style={{ color: '#1890ff' }}>5%</Title>
              <Text>Working Capital as % of Revenue</Text>
            </div>
          </Col>
        </Row>
      </Card>

      {/* Investment Recommendation */}
      <Card title="Investment Recommendation" className="dashboard-card" style={{ marginTop: 24 }}>
        <Alert
          message="Valuation Summary"
          description={
            <div>
              <p>
                Based on our analysis, the target company has an estimated enterprise value range of{' '}
                <strong>${(valuation_summary?.valuation_range?.low || 0).toLocaleString()}</strong> to{' '}
                <strong>${(valuation_summary?.valuation_range?.high || 0).toLocaleString()}</strong>.
              </p>
              <p>
                The DCF method provides the most reliable valuation at{' '}
                <strong>${(valuation_summary?.dcf_value || 0).toLocaleString()}</strong>, 
                supported by comparable company analysis and precedent transactions.
              </p>
              <p>
                <strong>Recommendation:</strong> Proceed with due diligence and consider the mid-point 
                valuation of <strong>${(((valuation_summary?.valuation_range?.low || 0) + (valuation_summary?.valuation_range?.high || 0)) / 2).toLocaleString()}</strong> 
                as the starting point for negotiations.
              </p>
            </div>
          }
          type="info"
          showIcon
        />
      </Card>
    </div>
  );
}

export default Valuation;
