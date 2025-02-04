import { Avatar, Badge, Empty, Flex, Table, type TableProps } from 'antd'
import React, { useState } from 'react'
import { UserData } from '../../types';

interface SubUsersTableProps {
    data: UserData[];
    isLoading: boolean;
}

type TableRowSelection<T extends object = object> = TableProps<T>['rowSelection'];

const SubUsersTable: React.FC<SubUsersTableProps> = ({ data, isLoading }) => {
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

    const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
        setSelectedRowKeys(newSelectedRowKeys);
    };

    const rowSelection: TableRowSelection<UserData> = {
        selectedRowKeys,
        onChange: onSelectChange,
        columnWidth: '60px',
        selections: [
            {
                key: 'selectAll',
                text: '選取全部',
                onSelect: () => {
                    setSelectedRowKeys(data.map((item) => item._id));
                },
            },
            {
                key: 'clear',
                text: '清空選取',
                onSelect: () => {
                    setSelectedRowKeys([]);
                },
            },
        ],
    };

    const columns: TableProps<UserData>['columns'] = [
        {
            title: '頭像',
            key: 'discord_url',
            align: 'center',
            width: 120,
            render: (data: UserData) => (
                <Avatar src={data.avatar} />
            )
        },
        {
            title: '名稱',
            dataIndex: 'discord_name',
            key: 'discord_name',
            align: 'center',
            width: 360
        },
        {
            title: 'ID',
            dataIndex: 'discord_id',
            key: 'discord_id',
            align: 'center',
            width: 360
        },
        {
            title: '總訂閱月數',
            dataIndex: 'total_amount',
            key: 'total_amount',
            align: 'center',
            width: 110
        },
        {
            title: '總訂閱金額',
            dataIndex: 'total_quantity',
            key: 'total_quantity',
            align: 'center',
            width: 110
        },
        {
            title: '身分組狀態',
            key: 'vmcount',
            align: 'center',
            render: (data: UserData) => (
                data.is_active ? (
                    <Badge status="success" text="活躍中" />
                ) : (
                    <Badge status="error" text="非活躍狀態" />
                )
            ),
        },
        {
            title: '加入日期',
            dataIndex: 'createAt',
            key: 'createAt',
            align: 'center',
            render: (timestamp: number) => {
                const date = new Date(timestamp * 1000);
                return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
            },
            width: 200
        },
    ];

    const [pageSize, setPageSize] = useState(20);
    const rowHeight = 60;

    return (
        <Table
            components={{
                header: {
                    row: (props: React.HTMLAttributes<HTMLTableRowElement>) => (
                        <tr {...props} style={{ height: '25px' }} />
                    ),
                },
            }}
            scroll={{ x: 'max-content', y: 495 }}
            rowSelection={rowSelection}
            columns={columns}
            dataSource={data}
            pagination={{
                position: ['bottomLeft'],
                pageSize: pageSize,
                pageSizeOptions: ['20', '50', '100', '9999'],
                showSizeChanger: true,
                onShowSizeChange: (_, size) => setPageSize(size),
            }}
            onRow={() => ({
                style: { height: rowHeight },
            })}
            rowKey={(record) => record._id}
            loading={isLoading}
            locale={{ emptyText: <Empty description="沒有明細" /> }}
        />
    )
}

export default SubUsersTable