import { Avatar, Empty, Table, type TableProps } from 'antd'
import React, { useState } from 'react'
import { Detail } from '../../types';

interface DetailsTableProps {
    data: Detail[];
    isLoading: boolean;
}

type TableRowSelection<T extends object = object> = TableProps<T>['rowSelection'];

const DetailTable: React.FC<DetailsTableProps> = ({ data, isLoading }) => {
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

    const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
        setSelectedRowKeys(newSelectedRowKeys);
    };

    const rowSelection: TableRowSelection<Detail> = {
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

    const columns: TableProps<Detail>['columns'] = [
        {
            title: '頭像',
            key: 'discord_url',
            align: 'center',
            width: 120,
            render: (data: Detail) => (
                <Avatar src={data.avatar}/>
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
            title: '訂閱日期',
            dataIndex: 'createAt',
            key: 'createAt',
            align: 'center',
            render: (timestamp: number) => {
                const date = new Date(timestamp * 1000);
                return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
            },
            width: 270
        },
        {
            title: '月數',
            dataIndex: 'quantity',
            key: 'quantity',
            align: 'center',
            width: 100
        },
        {
            title: '金額',
            dataIndex: 'amount',
            key: 'amount',
            align: 'center',
            width: 100
        },
        {
            title: '付款方式',
            dataIndex: 'payment',
            key: 'payment',
            align: 'center',
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

export default DetailTable