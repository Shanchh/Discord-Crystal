import { Button, Modal, Tooltip, Form, Input, Flex, message } from 'antd'
import React, { useState } from 'react'
import { EditOutlined } from '@ant-design/icons';
import { Detail, DetailModify } from '../../types';
import { modify_detail } from '../Api/HandleApi';

interface ModifyDetailBtnProps {
    data: Detail;
    handleModifyDetail: (values: DetailModify) => void;
}

const ModifyDetailBtn: React.FC<ModifyDetailBtnProps> = ({ data, handleModifyDetail }) => {
    const [form] = Form.useForm();
    const [modalOpen, setModal1Open] = useState<boolean>(false);

    function formatTimestampToDate(timestamp: number): string {
        const date = new Date(timestamp * 1000);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}-${month}-${day}`;
    }

    const handleSubmit = () => {
        const values: DetailModify = form.getFieldsValue();
        modify_detail(values)
            .then(() => {
                handleModifyDetail(values);
            })
            .catch(() => {
                message.error("修改明細失敗！")
            })
            .finally(() => {
                setModal1Open(false);
                message.success("修改明細成功！")
            })
    };

    return (
        <Tooltip title="編輯明細">
            <Button
                variant="link"
                color="default"
                onClick={() => {
                    setModal1Open(true);
                    form.setFieldsValue({
                        _id: data._id,
                        name: data.discord_name,
                        createTime: formatTimestampToDate(data.createAt),
                        payment: data.payment,
                        quantity: data.quantity,
                        amount: data.amount
                    });
                }}
            >
                <EditOutlined />
            </Button>
            <Modal
                title={
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <EditOutlined style={{ color: 'black' }} />
                        <span>編輯明細</span>
                    </div>
                }
                open={modalOpen}
                okText="保存"
                cancelText="取消"
                onOk={handleSubmit}
                onCancel={() => setModal1Open(false)}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleSubmit}
                >
                    <Form.Item
                        label="資料ID"
                        name="_id"
                        rules={[{ required: true }]}
                    >
                        <Input disabled />
                    </Form.Item>
                    <Form.Item
                        label="Discord名稱"
                        name="name"
                        rules={[{ required: true, message: '請填寫名稱' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Flex gap={20} style={{ width: '100%' }}>
                        <Form.Item
                            label="訂閱日期"
                            name="createTime"
                            style={{ flex: 1 }}
                            rules={[{ required: true, message: '請選擇訂閱日期' }]}
                        >
                            <Input />
                        </Form.Item>
                        <Form.Item
                            label="付款方式"
                            name="payment"
                            style={{ flex: 1 }}
                            rules={[{ required: true, message: '請輸入付款方式' }]}
                        >
                            <Input />
                        </Form.Item>
                    </Flex>
                    <Flex gap={20} style={{ width: '100%' }}>
                        <Form.Item
                            label="月數"
                            name="quantity"
                            style={{ flex: 1 }}
                            rules={[{ required: true, message: '請輸入月數' }, { pattern: /^\d+$/, message: '請輸入數字' }]}
                        >
                            <Input />
                        </Form.Item>
                        <Form.Item
                            label="金額"
                            name="amount"
                            style={{ flex: 1 }}
                            rules={[{ required: true, message: '請輸入金額' }, { pattern: /^\d+$/, message: '請輸入數字' }]}
                        >
                            <Input />
                        </Form.Item>
                    </Flex>
                </Form>
            </Modal>
        </Tooltip>
    );
}

export default ModifyDetailBtn