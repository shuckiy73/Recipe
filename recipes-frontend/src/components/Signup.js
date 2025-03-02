import { useState } from "react";
import { useAuth } from "../components/AuthContext";
import { TextField, Button, Container, Typography } from "@mui/material";

export default function Signup() {
  const { handleSignup } = useAuth();
  const [credentials, setCredentials] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await handleSignup(credentials.username, credentials.password);
  };

  return (
    <Container maxWidth="xs">
      <Typography variant="h4">Регистрация</Typography>
      <form onSubmit={handleSubmit}>
        <TextField fullWidth margin="normal" name="username" label="Логин" onChange={handleChange} />
        <TextField fullWidth margin="normal" type="password" name="password" label="Пароль" onChange={handleChange} />
        <Button type="submit" fullWidth variant="contained" color="secondary">Зарегистрироваться</Button>
      </form>
    </Container>
  );
}
