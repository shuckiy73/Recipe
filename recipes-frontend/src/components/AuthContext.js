import { createContext, useContext, useState, useEffect } from "react";
import { login, signup, logout } from "./api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) setUser({ token });
  }, []);

  const handleLogin = async (username, password) => {
    const data = await login(username, password);
    setUser({ token: data.auth_token });
  };

  const handleSignup = async (username, password) => {
    const data = await signup(username, password);
    setUser({ token: data.auth_token });
  };

  const handleLogout = () => {
    logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, handleLogin, handleSignup, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
