import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styled from "styled-components";

import { authApi } from "../services/api";
import { isAuthenticated } from "../utils/auth";

const Wrap = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${({ theme }) => theme.bg};
`;

const Card = styled.form`
  width: min(420px, 95vw);
  background: ${({ theme }) => theme.card};
  border-radius: 14px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const Input = styled.input`
  min-height: 42px;
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.soft};
  padding: 0 10px;
`;

const Btn = styled.button`
  min-height: 42px;
  border: none;
  border-radius: 8px;
  background: ${({ theme }) => theme.primary};
  color: #fff;
  cursor: pointer;
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
    <Wrap>
      <Card onSubmit={onSubmit}>
        <h2>Sign In</h2>
        <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p>{error}</p>}
        <Btn type="submit">Login</Btn>
        <p>
          New user? <Link to="/signup">Create an account</Link>
        </p>
      </Card>
    </Wrap>
  );
}

export default LoginPage;
