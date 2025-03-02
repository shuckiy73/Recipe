import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_URL,
});

export const login = async (username, password) => {
  const { data } = await api.post("/auth/token/login/", { username, password });
  localStorage.setItem("token", data.auth_token);
  api.defaults.headers.Authorization = `Token ${data.auth_token}`;
  return data;
};

export const signup = async (username, password) => {
  await api.post("/auth/users/", { username, password });
  return login(username, password);
};

export const logout = () => {
  localStorage.removeItem("token");
  delete api.defaults.headers.Authorization;
};
