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
            <Flex gap={10} justify='start' align='center' style={{ marginLeft: 10 }}>
                <span
                    onClick={navigateToHome}
                    style={{
                        fontSize: '34px',
                        fontWeight: 'bold',
                        fontFamily: '"Lucida Console", "微軟正黑體", "新細明體", sans-serif',
                        color: 'transparent',
                        backgroundImage: 'linear-gradient(90deg,rgb(189, 37, 37),rgb(4, 217, 255))',
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        cursor: 'pointer',
                        transition: 'transform 0.3s ease, textShadow 0.3s ease',
                    }}
                    onMouseOver={(e) => {
                        const target = e.target as HTMLElement;
                        target.style.transform = 'scale(1.1)';
                        target.style.textShadow = '0px 2px 4px rgba(0, 0, 0, 0.2)';
                    }}
                    onMouseOut={(e) => {
                        const target = e.target as HTMLElement;
                        target.style.transform = 'scale(1)';
                        target.style.textShadow = 'none';
                    }}
                >
                    CRYSTAL
                </span>
                <img src='assets/logo.png' style={{ height: 30 }}></img>
            </Flex>
        </Header>
    )
}

export default MainHeader