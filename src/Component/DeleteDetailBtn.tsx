import { Button, Tooltip } from 'antd'
import React from 'react'
import { DeleteOutlined } from '@ant-design/icons';

const DeleteDetailBtn = () => {
    return (
        <Tooltip title="刪除明細">
            <Button variant="link" color="danger">
                <DeleteOutlined />
            </Button>
        </Tooltip>
    )
}

export default DeleteDetailBtn