import { useState } from "react";
import styled from "styled-components";

const LoginWrapper = styled.div`
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
`;

const LoginCard = styled.form`
  width: 100%;
  max-width: 420px;
  background: ${({ theme }) => theme.card};
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 16px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-sizing: border-box;
`;

const Title = styled.h1`
  margin: 0;
  color: ${({ theme }) => theme.text};
  font-size: 30px;
  font-weight: 700;
`;

const Subtitle = styled.p`
  margin: 0 0 8px 0;
  color: ${({ theme }) => theme.soft2};
  font-size: 14px;
`;

const Label = styled.label`
  color: ${({ theme }) => theme.textSoft};
  font-size: 14px;
`;

const Input = styled.input`
  min-height: 44px;
  border-radius: 10px;
  border: 1px solid ${({ theme }) => theme.soft};
  background: ${({ theme }) => theme.bgDark};
  color: ${({ theme }) => theme.text};
  padding: 0 12px;
  outline: none;

  &:focus {
    border-color: ${({ theme }) => theme.primary};
  }
`;

const SignInButton = styled.button`
  margin-top: 6px;
  min-height: 46px;
  border: none;
  border-radius: 10px;
  background: ${({ theme }) => theme.primary};
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
`;

const ErrorText = styled.p`
  margin: 0;
  color: #ff7a7a;
  font-size: 13px;
`;

const HintText = styled.p`
  margin: 0;
  color: ${({ theme }) => theme.soft2};
  font-size: 12px;
`;

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!email.trim() || !password.trim()) {
      setError("Please enter your email and password.");
      return;
    }

    if (password.trim().length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setError("");
    onLogin(email.trim());
  };

  return (
    <LoginWrapper>
      <LoginCard onSubmit={handleSubmit}>
        <Title>Sign in</Title>
        <Subtitle>Log in to use the Brain Tumor Detector.</Subtitle>

        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="doctor@example.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        {error && <ErrorText>{error}</ErrorText>}
        <SignInButton type="submit">Sign In</SignInButton>
        <HintText>This is a frontend login screen for now.</HintText>
      </LoginCard>
    </LoginWrapper>
  );
}

export default LoginPage;
