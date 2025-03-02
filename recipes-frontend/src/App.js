import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./components/AuthContext";
import Login from "./components/Login";
import Signup from "./components/Signup";
import RecipeList from "./components/RecipeList";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/" element={<RecipeList />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
