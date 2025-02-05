import React from 'react'
import { Col, Flex, Row } from 'antd'
import OverviewStatisticsCard from '../../Component/OverviewStatisticsCard'
import { DollarOutlined, ClockCircleOutlined } from '@ant-design/icons';

const Dashboard = () => {
  return (
    <Flex vertical>
      <Row gutter={[16, 16]}>
        <Col md={12} xs={24}>
          <OverviewStatisticsCard value='total_quantity' cardTitle={<span><ClockCircleOutlined style={{ marginRight: 8 }} />總訂閱月數</span>} unitName='個月'/>
        </Col>
        <Col md={12} xs={24}>
          <OverviewStatisticsCard value='total_amount' cardTitle={<span><DollarOutlined style={{ marginRight: 8 }} />總訂閱金額</span>} unitName='元'/>
        </Col>
      </Row>
    </Flex>
  )
}

export default Dashboard