import { Link } from "react-router-dom";
import styled from "styled-components";

const Wrap = styled.div`
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: ${({ theme }) => theme.bg};
`;

const Card = styled.div`
  width: min(760px, 100%);
  background: ${({ theme }) => theme.card};
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 16px;
  padding: 28px;
  text-align: center;
`;

const Title = styled.h1`
  margin: 0;
  color: ${({ theme }) => theme.text};
`;

const Desc = styled.p`
  margin: 14px 0 0;
  color: ${({ theme }) => theme.textSoft};
  line-height: 1.6;
`;

const Actions = styled.div`
  margin-top: 24px;
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
`;

const Btn = styled(Link)`
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  color: ${({ theme, $secondary }) => ($secondary ? theme.text : "#fff")};
  background: ${({ theme, $secondary }) => ($secondary ? "transparent" : theme.primary)};
  border: 1px solid ${({ theme, $secondary }) => ($secondary ? theme.soft : "transparent")};
`;

function HomePage() {
  return (
    <Wrap>
      <Card>
        <Title>AI-Powered Brain Tumor Detection System</Title>
        <Desc>
          Detect and classify brain tumors from MRI scans with AI support, manage patient records,
          review prediction history, and generate professional clinical reports.
        </Desc>
        <Actions>
          <Btn to="/login">Login</Btn>
          <Btn to="/signup" $secondary>
            Sign Up
          </Btn>
        </Actions>
      </Card>
    </Wrap>
  );
}

export default HomePage;
