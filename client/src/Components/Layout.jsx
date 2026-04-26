import { Link, useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";

const Wrapper = styled.div`
  min-height: 100vh;
  display: flex;
  background: ${({ theme }) => theme.bg};
  color: ${({ theme }) => theme.text};
`;

const Sidebar = styled.aside`
  width: 250px;
  background: ${({ theme }) => theme.card};
  border-right: 1px solid ${({ theme }) => theme.bgLighter};
  padding: 20px;
  box-sizing: border-box;
  @media (max-width: 900px) {
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    display: flex;
    gap: 10px;
    z-index: 20;
  }
`;

const Brand = styled.h2`
  margin: 0 0 18px 0;
  font-size: 18px;
  @media (max-width: 900px) {
    display: none;
  }
`;

const NavItem = styled(Link)`
  display: block;
  padding: 10px 12px;
  margin-bottom: 8px;
  text-decoration: none;
  border-radius: 8px;
  color: ${({ theme, $active }) => ($active ? "#fff" : theme.text)};
  background: ${({ theme, $active }) => ($active ? theme.primary : "transparent")};
  font-weight: 600;
`;

const Content = styled.main`
  flex: 1;
  padding: 24px;
  margin-bottom: 70px;
`;

const TopRow = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
`;

const Logout = styled.button`
  border: 1px solid ${({ theme }) => theme.soft};
  background: transparent;
  color: ${({ theme }) => theme.text};
  border-radius: 8px;
  min-height: 38px;
  padding: 0 14px;
  cursor: pointer;
`;

function AppLayout({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const active = location.pathname;

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <Wrapper>
      <Sidebar>
        <Brand>Brain Tumor AI</Brand>
        <NavItem to="/patient-info" $active={active === "/patient-info" || active === "/dashboard"}>
          Patient Info
        </NavItem>
        <NavItem to="/prediction" $active={active === "/prediction"}>
          Prediction
        </NavItem>
        <NavItem to="/history" $active={active === "/history"}>
          History
        </NavItem>
      </Sidebar>
      <Content>
        <TopRow>
          <Logout onClick={handleLogout}>Logout</Logout>
        </TopRow>
        {children}
      </Content>
    </Wrapper>
  );
}

export default AppLayout;
