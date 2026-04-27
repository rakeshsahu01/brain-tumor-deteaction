import { Link } from "react-router-dom";
import styled from "styled-components";

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #2d1b4e 100%);
  overflow: hidden;
`;

const Header = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 40px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;

  @media (max-width: 768px) {
    padding: 16px 20px;
  }
`;

const Logo = styled.div`
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;

  span {
    background: linear-gradient(90deg, #00d4ff, #854CE6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
`;

const Nav = styled.nav`
  display: flex;
  gap: 32px;
  align-items: center;

  @media (max-width: 768px) {
    display: none;
  }

  a {
    color: #c1c7c9;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: color 0.3s ease;

    &:hover {
      color: #00d4ff;
    }
  }
`;

const HeaderButtons = styled.div`
  display: flex;
  gap: 12px;
  align-items: center;

  @media (max-width: 768px) {
    gap: 8px;
  }
`;

const HeaderBtn = styled(Link)`
  padding: 10px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  ${({ $primary }) =>
    $primary
      ? `
    background: linear-gradient(90deg, #00d4ff, #854CE6);
    color: #fff;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(0, 212, 255, 0.3);
    }
  `
      : `
    color: #fff;
    background: transparent;
    border: 1px solid #854CE6;
    
    &:hover {
      background: rgba(133, 76, 230, 0.1);
    }
  `}

  @media (max-width: 768px) {
    padding: 8px 16px;
    font-size: 12px;
  }
`;

const HeroSection = styled.section`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  padding: 60px 40px;
  text-align: center;
  max-width: 1000px;
  margin: 0 auto;

  @media (max-width: 768px) {
    padding: 40px 20px;
    min-height: auto;
  }
`;

const Badge = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  padding: 8px 16px;
  border-radius: 20px;
  margin-bottom: 24px;
  color: #00d4ff;
  font-size: 13px;
  font-weight: 500;

  @media (max-width: 768px) {
    margin-bottom: 16px;
  }
`;

const Title = styled.h1`
  font-size: 56px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 24px 0;
  line-height: 1.2;
  letter-spacing: -1px;

  @media (max-width: 768px) {
    font-size: 36px;
  }

  @media (max-width: 480px) {
    font-size: 28px;
  }
`;

const HighlightText = styled.span`
  background: linear-gradient(90deg, #00d4ff, #854CE6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  font-size: 18px;
  color: #c1c7c9;
  margin: 0 0 48px 0;
  line-height: 1.6;
  max-width: 600px;

  @media (max-width: 768px) {
    font-size: 16px;
    margin-bottom: 32px;
  }
`;

const CTA = styled.div`
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
`;

const CTABtn = styled(Link)`
  padding: 14px 32px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  ${({ $primary }) =>
    $primary
      ? `
    background: linear-gradient(90deg, #00d4ff, #854CE6);
    color: #fff;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 40px rgba(0, 212, 255, 0.3);
    }
  `
      : `
    color: #fff;
    background: transparent;
    border: 2px solid #00d4ff;
    
    &:hover {
      background: rgba(0, 212, 255, 0.1);
      transform: translateY(-2px);
    }
  `}

  @media (max-width: 768px) {
    padding: 12px 24px;
    font-size: 14px;
  }
`;

function HomePage() {
  return (
    <Container>
      <Header>
        <Logo>
          🧠 <span>BTD</span>
        </Logo>
        <Nav>
          <a href="#features">Features</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </Nav>
        <HeaderButtons>
          <HeaderBtn to="/login">Login</HeaderBtn>
          <HeaderBtn to="/signup" $primary>
            Get Started
          </HeaderBtn>
        </HeaderButtons>
      </Header>

      <HeroSection>
        <Badge>
          <span>⚡</span>
          AI-Powered Medical Detection
        </Badge>
        <Title>
          Detect brain tumors with <HighlightText>advanced AI</HighlightText> precision
        </Title>
        <Subtitle>
          Upload MRI scans and receive instant AI-powered analysis. Manage patient records,
          review prediction history, and generate comprehensive clinical reports with ease.
        </Subtitle>
        <CTA>
          <CTABtn to="/signup" $primary>
            Get Started →
          </CTABtn>
          <CTABtn to="/login">
            ↗ Try Demo
          </CTABtn>
        </CTA>
      </HeroSection>
    </Container>
  );
}

export default HomePage;
