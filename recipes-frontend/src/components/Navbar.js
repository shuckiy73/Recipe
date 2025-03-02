import { AppBar, Toolbar, Button } from "@mui/material";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, handleLogout } = useAuth();
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Button color="inherit" onClick={() => navigate("/")}>Рецепты</Button>
        {user ? (
          <Button color="inherit" onClick={handleLogout}>Выход</Button>
        ) : (
          <>
            <Button color="inherit" onClick={() => navigate("/login")}>Вход</Button>
            <Button color="inherit" onClick={() => navigate("/signup")}>Регистрация</Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}
