import React, { useEffect, useState } from 'react'
import { get_all_detail_lists } from '../../Api/HandleApi';
import { Detail } from '../../../types'
import DetailTable from '../../Component/DetailsTable';
import { ReloadOutlined, UserOutlined, SearchOutlined, IdcardOutlined } from '@ant-design/icons';
import { Button, Col, DatePicker, Flex, Form, Input, Radio, Row, Select } from 'antd';

type Filter = {
  id: string;
  name: string;
  payment: string;
  createMonth: Date;
}

type SelectOption = {
  value: string;
  label: string;
}

const DetailManage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userListData, setUserListData] = useState<Detail[]>([]);
  const [searchLoading, setSearchLoading] = useState<boolean>(false);

  const [selectType, setSelectType] = useState<string>('none');
  const [sortType, setSortType] = useState<string>('none');

  const [filterUserListData, setFilterUserListData] = useState<Detail[]>([]);

  const refreshData = async () => {
    setIsLoading(true);
    const data = await get_all_detail_lists();
    setUserListData(data);
    setFilterUserListData(data);
    setIsLoading(false);
  };

  useEffect(() => {
    refreshData();
  }, []);

  const selectOption = [
    { value: 'none', label: '選擇種類' },
    { value: 'createAt', label: '訂閱日期' },
    { value: 'quantity', label: '月數' },
    { value: 'amount', label: '金額' }
  ];

  const NoneSorterOption = [
    { value: 'none', label: '選擇排序方式' }
  ];

  const dateSortOption = [
    { value: 'none', label: '選擇排序方式' },
    { value: 'descending', label: '從近到遠' },
    { value: 'ascending', label: '從遠到近' }
  ]

  const sortOption = [
    { value: 'none', label: '選擇排序方式' },
    { value: 'descending', label: '從高到低' },
    { value: 'ascending', label: '從低到高' }
  ]

  const [selectSorterOption, setSelectSorterOption] = useState<SelectOption[]>(NoneSorterOption);

  const handleTypeChange = (value: string) => {
    setSelectType(value);
  
    if (value === 'none') {
      setSelectSorterOption(NoneSorterOption);
    } else if (value === 'createAt') {
      setSelectSorterOption(dateSortOption);
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

  function getMonthTimestamps(now: any) {
    const validDate = now?.toDate ? now.toDate() : now instanceof Date ? now : new Date();
  
    const startOfMonth = Math.floor(new Date(validDate.getFullYear(), validDate.getMonth(), 1).getTime() / 1000);
    const endOfMonth = Math.floor((new Date(validDate.getFullYear(), validDate.getMonth() + 1, 1).getTime() - 1) / 1000);
  
    return { startOfMonth, endOfMonth };
  }

  const onSubmit = (values: Filter) => {
    setSearchLoading(true);
    const { id, name, payment, createMonth } = values;
  
    const { startOfMonth, endOfMonth } = createMonth
      ? getMonthTimestamps(createMonth)
      : { startOfMonth: 0, endOfMonth: Infinity };
  
    const filtered = userListData.filter((item) => {
      const matchId = id ? item.discord_id.includes(id) : true;
      const matchName = name ? item.discord_name.includes(name) : true;
      const matchPayment = payment === 'all' || payment.toUpperCase() === item.payment.toUpperCase();
      const matchDate = startOfMonth <= item.createAt && item.createAt <= endOfMonth;
  
      return matchId && matchName && matchPayment && matchDate;
    });
  
    let sortedData = [...filtered];
  
    if (selectType !== 'none' && sortType !== 'none') {
      const sortKey = selectType as keyof Pick<Detail, 'createAt' | 'quantity' | 'amount'>;
      const sortOrder = sortType === 'ascending' ? 1 : -1;
  
      sortedData.sort((a, b) => (a[sortKey] - b[sortKey]) * sortOrder);
    }
  
    setFilterUserListData(sortedData);
    setSearchLoading(false);
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
            <Form.Item name="payment" initialValue={'all'}>
              <Flex justify="start" align="center" gap={5}>
                <h3>付款方式：</h3>
                <Radio.Group defaultValue="all">
                  <Radio.Button value="all">全選</Radio.Button>
                  <Radio.Button value={"銀行轉帳"}>銀行轉帳</Radio.Button>
                  <Radio.Button value={"PayPal"}>PayPal</Radio.Button>
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
          <Col>
            <Flex justify="start" align="center" gap={10}>
              <h3>時間範圍：</h3>
              <Form.Item name="createMonth" style={{ margin: 0 }}>
                <DatePicker placeholder='選擇月份' picker="month" />
              </Form.Item>
            </Flex>
          </Col>
        </Row>
        <Flex justify="end" style={{ paddingTop: 10 }} gap={10}>
          <Button htmlType="submit" type="primary" icon={<SearchOutlined />} loading={searchLoading}>
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
      <DetailTable data={filterUserListData} isLoading={isLoading} />
    </Flex>

  )
}

export default DetailManage