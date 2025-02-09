import React from "react";
import "../pages/HomePage.css";
import { Button } from "../components/Button";

export const HomePage: React.FC = () => {
  return (
    <div className="home-container">
      <h1 className="greeting">Welcome to Our Amazing App!</h1>
      <Button to="/app">Go to App</Button>
      <Button to="/history">Go to History</Button>
    </div>
  );
};
