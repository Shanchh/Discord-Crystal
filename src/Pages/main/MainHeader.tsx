import { Flex, Layout } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Header } = Layout;

const MainHeader = () => {
    const navigate = useNavigate();

    const navigateToHome = () => {
        navigate("/");
    };

    return (
        <Header style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: '#f6f8f5',
            height: '50px',
            borderBottom: '2px solid #ffffff',
            padding: '0',
        }}>
            <Flex gap={5} justify='start' align='center' style={{ marginLeft: 10 }}>
                <img src='assets/logo.png' style={{ height: 30 }}></img>
                <span onClick={navigateToHome} style={{ fontSize: 34, fontWeight: 'bold', fontFamily: "Lucida Console, 微軟正黑體, 新細明體, sans-serif" }}>CRYSTAL</span>
            </Flex>
        </Header>
    )
}

export default MainHeader