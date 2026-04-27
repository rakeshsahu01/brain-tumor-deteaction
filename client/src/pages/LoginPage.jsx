import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styled from "styled-components";

import { authApi } from "../services/api";
import { isAuthenticated } from "../utils/auth";

const Container = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #2d1b4e 100%);
  padding: 20px;
`;

const Card = styled.form`
  width: min(420px, 95vw);
  background: rgba(28, 30, 39, 0.8);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 16px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  backdrop-filter: blur(10px);
`;

const Title = styled.h2`
  margin: 0;
  color: #fff;
  font-size: 28px;
  font-weight: 700;
  text-align: center;
`;

const Subtitle = styled.p`
  margin: 0;
  color: #c1c7c9;
  font-size: 14px;
  text-align: center;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

const Label = styled.label`
  color: #c1c7c9;
  font-size: 13px;
  font-weight: 500;
`;

const Input = styled.input`
  min-height: 42px;
  border-radius: 8px;
  border: 1px solid rgba(0, 212, 255, 0.3);
  padding: 0 14px;
  background: rgba(0, 0, 0, 0.2);
  color: #fff;
  font-size: 14px;
  transition: all 0.3s ease;

  &::placeholder {
    color: #909190;
  }

  &:focus {
    outline: none;
    border-color: #00d4ff;
    background: rgba(0, 212, 255, 0.05);
  }
`;

const Btn = styled.button`
  min-height: 42px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(90deg, #00d4ff, #854CE6);
  color: #fff;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.3s ease;
  margin-top: 8px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 212, 255, 0.3);
  }

  &:active {
    transform: translateY(0);
  }
`;

const ErrorMsg = styled.p`
  background: rgba(255, 59, 48, 0.1);
  border: 1px solid rgba(255, 59, 48, 0.3);
  color: #ff3b30;
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 13px;
  margin: 0;
`;

const Footer = styled.p`
  margin: 0;
  color: #c1c7c9;
  font-size: 13px;
  text-align: center;

  a {
    color: #00d4ff;
    text-decoration: none;
    font-weight: 600;

    &:hover {
      text-decoration: underline;
    }
  }
`;

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated()) {
      navigate("/dashboard", { replace: true });
    }
  }, [navigate]);

  const onSubmit = async (event) => {
    event.preventDefault();
    try {
      const res = await authApi.login({ email, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      navigate("/dashboard");
    } catch (err) {
      setError(err?.response?.data?.message || "Login failed");
    }
  };

  return (
    <Container>
      <Card onSubmit={onSubmit}>
        <Title>Welcome Back</Title>
        <Subtitle>Sign in to your BTD account</Subtitle>
        
        <InputGroup>
          <Label>Email Address</Label>
          <Input 
            type="email" 
            placeholder="you@example.com" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
        </InputGroup>

        <InputGroup>
          <Label>Password</Label>
          <Input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </InputGroup>

        {error && <ErrorMsg>{error}</ErrorMsg>}
        
        <Btn type="submit">Sign In</Btn>
        
        <Footer>
          Don't have an account? <Link to="/signup">Sign up for free</Link>
        </Footer>
      </Card>
    </Container>
  );
}

export default LoginPage;
