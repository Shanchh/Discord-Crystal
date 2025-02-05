import React, { useState } from 'react';
import { Layout, theme, Grid } from 'antd';
import { Outlet } from 'react-router';
import { Content } from 'antd/es/layout/layout';
import OptionList from './OptionList';
import MainHeader from './MainHeader';
import MainBreadcrumb from './MainBreadcrumb';

const { Sider } = Layout;

const EmptyPage: React.FC = () => {

    const {
        token: { colorBgContainer, borderRadiusLG },
    } = theme.useToken();

    return (
        <Layout style={{ height: '100vh', width: '100%' }}>
            <MainHeader />
            <Layout>
                <Sider
                    width={200}
                    collapsedWidth={0}
                    style={{
                        background: colorBgContainer,
                        transition: 'all 0.3s ease',
                        overflow: 'hidden',
                    }}
                >
                    <OptionList />
                </Sider>
                <Layout style={{ padding: '0 24px 24px' }}>
                    <MainBreadcrumb />
                    <Content
                        style={{
                            flex: 1,
                            display: 'flex',
                            flexDirection: 'column',
                            margin: 0,
                            borderRadius: borderRadiusLG,
                        }}
                    >
                        <Outlet />
                    </Content>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default EmptyPage;