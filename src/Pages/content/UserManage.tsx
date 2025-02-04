import React, { useEffect, useState } from 'react'
import SubUsersTable from '../../Component/SubUsersTable'
import { UserData } from '../../../types';
import { get_all_user_data } from '../../Api/HandleApi';

const UserManage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userListData, setUserListData] = useState<UserData[]>([]);
  const [searchLoading, setSearchLoading] = useState<boolean>(false);

  const refreshData = async () => {
    setIsLoading(true);
    const data = await get_all_user_data();
    setUserListData(data);
    setIsLoading(false);
  };

  useEffect(() => {
    refreshData();
  }, []);

  return (
    <SubUsersTable data={userListData} isLoading={isLoading} />
  )
}

export default UserManage