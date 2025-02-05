import { Card, Flex, Spin, theme } from 'antd'
import React, { ReactNode, useEffect, useState } from 'react'
import { get_statistics } from '../Api/HandleApi';

interface OverviewStatisticsCardProps {
    value: string;
    cardTitle: ReactNode;
    unitName: string;
}

const OverviewStatisticsCard: React.FC<OverviewStatisticsCardProps> = ({ value, cardTitle, unitName }) => {
    const { token } = theme.useToken();
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [showValue, setShowValue] = useState<string>('0');

    const refreshData = async () => {
        setIsLoading(true);
        const data = await get_statistics(value);
        setShowValue(data);
        setIsLoading(false);
    };

    useEffect(() => {
        refreshData()
    }, []);

    return (
        <Card title={cardTitle}>
            <Flex justify="center" align="center">
                <h1 style={{ color: token.colorPrimaryActive }}>
                    {isLoading ? (
                        <Spin size="large" />
                    ) : (
                        showValue + " " + unitName
                    )}
                </h1>
            </Flex>
        </Card>
    )
}

export default OverviewStatisticsCard