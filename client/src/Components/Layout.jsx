import { Link, useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";

const Wrapper = styled.div`
  min-height: 100vh;
  display: flex;
  background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #2d1b4e 100%);
  color: ${({ theme }) => theme.text};
`;

const Sidebar = styled.aside`
  width: 280px;
  background: rgba(28, 30, 39, 0.8);
  border-right: 1px solid rgba(0, 212, 255, 0.2);
  padding: 24px;
  box-sizing: border-box;
  backdrop-filter: blur(10px);
  
  @media (max-width: 900px) {
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    display: flex;
    gap: 10px;
    z-index: 20;
    padding: 12px;
    border-right: none;
    border-top: 1px solid rgba(0, 212, 255, 0.2);
  }
`;

const Brand = styled.h2`
  margin: 0 0 28px 0;
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(90deg, #00d4ff, #854CE6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 900px) {
    display: none;
  }
`;

const NavItem = styled(Link)`
  display: block;
  padding: 12px 16px;
  margin-bottom: 10px;
  text-decoration: none;
  border-radius: 10px;
  color: ${({ $active }) => ($active ? "#fff" : "#c1c7c9")};
  background: ${({ $active }) => 
    $active 
      ? "linear-gradient(90deg, rgba(0, 212, 255, 0.2), rgba(133, 76, 230, 0.2))" 
      : "transparent"
  };
  border: ${({ $active }) => 
    $active 
      ? "1px solid rgba(0, 212, 255, 0.3)" 
      : "1px solid transparent"
  };
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    background: rgba(0, 212, 255, 0.1);
    border-color: rgba(0, 212, 255, 0.3);
    color: #fff;
  }

  @media (max-width: 900px) {
    margin-bottom: 0;
    flex: 1;
    text-align: center;
    margin: 0 4px;
    padding: 10px 12px;
  }
`;

const Content = styled.main`
  flex: 1;
  padding: 28px;
  margin-bottom: 70px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  box-sizing: border-box;

  @media (max-width: 900px) {
    padding: 16px;
    margin-bottom: 90px;
  }
`;

const TopRow = styled.div`
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 28px;
  gap: 12px;
`;

const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  color: #c1c7c9;
  font-size: 13px;
  margin-right: 12px;
  border-right: 1px solid rgba(0, 212, 255, 0.2);
  padding-right: 12px;
`;

const UserName = styled.span`
  color: #fff;
  font-weight: 600;
  font-size: 14px;
`;

const Logout = styled.button`
  border: 1px solid rgba(0, 212, 255, 0.3);
  background: transparent;
  color: #c1c7c9;
  border-radius: 8px;
  min-height: 38px;
  padding: 0 16px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.3s ease;

  &:hover {
    border-color: #ff3b30;
    color: #ff3b30;
    background: rgba(255, 59, 48, 0.1);
  }

  @media (max-width: 900px) {
    min-height: 36px;
    padding: 0 12px;
    font-size: 12px;
  }
`;

function AppLayout({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const active = location.pathname;
  
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <Wrapper>
      <Sidebar>
        <Brand>🧠 BTD</Brand>
        <NavItem to="/patient-info" $active={active === "/patient-info" || active === "/dashboard"}>
          📋 Patient Info
        </NavItem>
        <NavItem to="/prediction" $active={active === "/prediction"}>
          🔍 Prediction
        </NavItem>
        <NavItem to="/history" $active={active === "/history"}>
          📊 History
        </NavItem>
      </Sidebar>
      <Content>
        <TopRow>
          <UserInfo>
            <UserName>{user?.name || "User"}</UserName>
            <span>{user?.email || "user@example.com"}</span>
          </UserInfo>
          <Logout onClick={handleLogout}>Logout</Logout>
        </TopRow>
        {children}
      </Content>
    </Wrapper>
  );
}

export default AppLayout;
