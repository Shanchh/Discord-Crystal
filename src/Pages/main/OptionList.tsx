import React from 'react'
import { Menu } from 'antd';
import { UserOutlined, DashboardOutlined, HomeOutlined, OrderedListOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useLocation, useNavigate } from "react-router-dom"

const OptionList = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const item3: MenuProps['items'] = [
        {
            key: '/',
            icon: <HomeOutlined />,
            label: '首頁',
            onClick: () => navigate("/"),
        },
        {
            key: '/dashboard',
            icon: <DashboardOutlined />,
            label: '儀錶板',
            onClick: () => navigate("/dashboard"),
        },
        {
            key: '/user-manage',
            icon: <UserOutlined />,
            label: '用戶列表',
            onClick: () => navigate("/user-manage"),
        },
        {
            key: '/detail-manage',
            icon: <OrderedListOutlined />,
            label: '訂閱明細',
            onClick: () => navigate("/detail-manage"),
        }
    ];
    return (
        <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            defaultSelectedKeys={['/home']}
            style={{ height: '100%', borderRight: 0 }}
            items={item3}
        />
    )
}

export default OptionList