import React, { useState } from "react";
import LoginForm from "./components/Auth/LoginForm";
import RegisterForm from "./components/Auth/RegisterForm";
import MainBoard from "./components/MainBoard";
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("accessToken"));

  const handleLogin = (data) => {
    setIsLoggedIn(true);
  };

  const handleRegister = (data) => {
    // Możesz dodać automatyczne logowanie po rejestracji
  };

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setIsLoggedIn(false);
  };

  if (isLoggedIn) {
    return <MainBoard onLogout={handleLogout} />;
  }

  return (
    <div className="App">
      <LoginForm onLogin={handleLogin} />
      <RegisterForm onRegister={handleRegister} />
    </div>
  );
}

export default App;
