import React, { useEffect, useState } from 'react'
import SubUsersTable from '../../Component/SubUsersTable'
import { UserData } from '../../../types';
import { get_all_user_data } from '../../Api/HandleApi';
import { Button, Col, Flex, Form, Input, Radio, Row, Select } from 'antd';
import { UserOutlined, SearchOutlined, IdcardOutlined, ReloadOutlined } from '@ant-design/icons';

type Filter = {
  id: string;
  name: string;
  is_active: string;
}

type SelectOption = {
  value: string;
  label: string;
}

const UserManage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userListData, setUserListData] = useState<UserData[]>([]);

  const [selectType, setSelectType] = useState<string>('none');
  const [sortType, setSortType] = useState<string>('none');

  const [filterUserListData, setFilterUserListData] = useState<UserData[]>([]);

  const refreshData = async () => {
    setIsLoading(true);
    const data = await get_all_user_data();
    setUserListData(data);
    setFilterUserListData(data);
    setIsLoading(false);
  };

  useEffect(() => {
    refreshData();
  }, []);

  const NoneSorterOption = [
    { value: 'none', label: '選擇排序方式' }
  ];

  const selectOption = [
    { value: 'none', label: '選擇種類' },
    { value: 'total_quantity', label: '總月數' },
    { value: 'total_amount', label: '總金額' }
  ];

  const sortOption = [
    { value: 'none', label: '選擇排序方式' },
    { value: 'descending', label: '從高到低' },
    { value: 'ascending', label: '從低到高' }
  ];

  const [selectSorterOption, setSelectSorterOption] = useState<SelectOption[]>(NoneSorterOption);

  const handleTypeChange = (value: string) => {
    setSelectType(value);
    if (value === 'none') {
      setSelectSorterOption(NoneSorterOption);
    } else {
      setSelectSorterOption(sortOption);
    }
    setSortType('none');
  };

  const clearSearch = () => {
    setSelectType('none');
    setSortType('none');
    setFilterUserListData(userListData);
  };

  const onSubmit = (values: Filter) => {
    console.log("123", selectType, sortType);
    const { id, name, is_active } = values;

    const filtered = userListData.filter((item) => {
      const matchId = id ? item.discord_id.includes(id) : true;
      const matchName = name ? item.discord_name.includes(name) : true;
      const matchActive =
        is_active === 'all' || item.is_active === (is_active === 'true');

      return matchId && matchName && matchActive;
    });

    let sortedData = [...filtered];

    if (selectType !== 'none' && sortType !== 'none') {
      const sortKey = selectType as keyof Pick<UserData, 'total_quantity' | 'total_amount'>;
      const sortOrder = sortType === 'ascending' ? 1 : -1;
      sortedData.sort((a, b) => (a[sortKey] - b[sortKey]) * sortOrder);
    }

    setFilterUserListData(sortedData);
  };

  return (
    <Flex vertical justify='center' align='center' gap={10} style={{ width: '100%' }}>
      <Form
        name="detail_search"
        layout="vertical"
        onFinish={(values) => onSubmit(values)}
        style={{ width: '100%', padding: '0 10px 0 10px' }}
      >
        <Row justify="start" gutter={22}>
          <Col>
            <Form.Item name="name" initialValue={''}>
              <Flex justify="start" align="center" gap={10}>
                <h3>用戶名稱：</h3>
                <Input placeholder="請輸入名稱" prefix={<UserOutlined />} style={{ width: 230 }} />
              </Flex>
            </Form.Item>
          </Col>
          <Col>
            <Form.Item name="id" initialValue={''}>
              <Flex justify="start" align="center" gap={10}>
                <h3>用戶ID：</h3>
                <Input placeholder="請輸入ID" prefix={<IdcardOutlined />} style={{ width: 230 }} />
              </Flex>
            </Form.Item>
          </Col>
          <Col>
            <Form.Item name="is_active" initialValue={'all'}>
              <Flex justify="start" align="center" gap={5}>
                <h3>身分組狀態：</h3>
                <Radio.Group defaultValue="all">
                  <Radio.Button value="all">全選</Radio.Button>
                  <Radio.Button value={"true"}>啟用中</Radio.Button>
                  <Radio.Button value={"false"}>未啟用</Radio.Button>
                </Radio.Group>
              </Flex>
            </Form.Item>
          </Col>
          <Col>
            <Form.Item>
              <Flex justify="start" align="center" gap={10}>
                <h3>排序：</h3>
                <Select
                  size="middle"
                  defaultValue="none"
                  value={selectType}
                  style={{ width: 120 }}
                  onChange={(value) => handleTypeChange(value)}
                  options={selectOption}
                />

                <Select
                  size="middle"
                  defaultValue="none"
                  style={{ width: 128 }}
                  options={selectSorterOption}
                  value={sortType}
                  onChange={(value) => setSortType(value)}
                />
              </Flex>
            </Form.Item>
          </Col>
        </Row>
        <Flex justify="end" style={{ paddingTop: 10 }} gap={10}>
          <Button htmlType="submit" type="primary" icon={<SearchOutlined />}>
            條件查詢
          </Button>
          <Button htmlType="reset" type="default" onClick={() => clearSearch()}>
            清除條件
          </Button>
        </Flex>
      </Form>

      <Flex justify='flex-start' align='center' style={{ width: '100%' }}>
        <Button color="default" variant="outlined" icon={<ReloadOutlined />} onClick={() => refreshData()}>刷新表格</Button>
      </Flex>
      <SubUsersTable data={filterUserListData} isLoading={isLoading} />
    </Flex>
  )
}

export default UserManage