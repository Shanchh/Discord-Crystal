import { Avatar, Button, Flex, message, Modal, Tooltip } from 'antd'
import React, { useState } from 'react'
import { DeleteOutlined } from '@ant-design/icons';
import { Detail } from '../../types';
import { delete_detail } from '../Api/HandleApi';

interface DeleteDetailBtnProps {
    data: Detail;
    handleDelete: (id: string) => void;
}

const DeleteDetailBtn: React.FC<DeleteDetailBtnProps> = ({ data, handleDelete }) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const onDelete = () => {
        setIsLoading(true);
        delete_detail(data._id)
            .then(() => {
                handleDelete(data._id);
                message.success("明細刪除成功！");
            })
            .finally(() => {
                setIsLoading(false);
            })
    };

    return (
        <Tooltip title="刪除明細">
            <Button variant="link" color="danger" onClick={() => setModalOpen(true)}>
                <DeleteOutlined />
            </Button>
            <Modal
                centered
                title={
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Avatar src={data.avatar} />
                        <span>刪除明細</span>
                    </div>
                }
                open={modalOpen}
                width={330}
                onCancel={() => setModalOpen(false)}
                footer={null}
            >
                <span style={{fontWeight:'bold'}}>確認是否刪除這筆 {data.discord_name} 的明細？</span>
                <Flex justify='flex-end' gap={5} style={{ paddingTop: 10 }}>
                    <Button color="default" variant="outlined" style={{ fontSize: 16 }} onClick={() => setModalOpen(false)}>
                        取消
                    </Button>
                    <Button color="primary" variant="solid" style={{ fontSize: 16 }} loading={isLoading} onClick={() => onDelete()}>
                        確認
                    </Button>
                </Flex>
            </Modal>
        </Tooltip>
    )
}

export default DeleteDetailBtn