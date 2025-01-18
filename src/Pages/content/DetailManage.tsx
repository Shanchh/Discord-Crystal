import React, { useEffect, useState } from 'react'
import { get_all_detail_lists } from '../../Api/HandleApi';
import { Detail } from '../../../types'
import DetailTable from '../../Component/DetailsTable';
import { ReloadOutlined } from '@ant-design/icons';
import { Button, Flex } from 'antd';

const DetailManage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userListData, setUserListData] = useState<Detail[]>([]);

  const refreshData = async () => {
    setIsLoading(true);
    const data = await get_all_detail_lists();
    setUserListData(data);
    setIsLoading(false);
  };

  useEffect(() => {
    refreshData();
  }, []);

  return (
    <Flex vertical justify='center' align='center' gap={10} style={{ width: '100%' }}>
      <Flex justify='flex-start' align='center' style={{ width: '100%' }}>
        <Button color="default" variant="outlined" icon={<ReloadOutlined />} onClick={() => refreshData()}>刷新表格</Button>
      </Flex>
      <DetailTable data={userListData} isLoading={isLoading}/>
    </Flex>

  )
}

export default DetailManage