import { Avatar, Flex } from 'antd'
import React from 'react'

const Home = () => {
  return (
    <Flex gap={15} vertical justify="center" align="center" style={{ height: '100%', width: '100%' }}>
      <Avatar size={200} shape="square" src="assets/shanchh.jpg" />
      <span
        style={{ fontSize: '50px', fontWeight: 'bold', color: 'black', textShadow: '2px 2px 4px rgba(0, 0, 0, 0.6)', letterSpacing: '2px' }}>
        DISCORD-CRYSTAL
      </span>
      <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#1890ff', textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)' }}>
        Created by Shanchh, 2025
      </span>
      <Flex gap={15} style={{ marginTop: 10 }}>
        <a href="https://github.com/Shanchh/Discord-Crystal" target="_blank" rel="noopener noreferrer">
          <Avatar size={50} src='assets/github.png' />
        </a>
        <a href="https://discord.com/users/316548382308958208" target="_blank" rel="noopener noreferrer">
          <Avatar size={50} src='assets/discord.png' />
        </a>
      </Flex>
    </Flex>
  );
}

export default Home