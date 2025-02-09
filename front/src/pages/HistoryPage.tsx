import React from "react";
import { useNavigate } from "react-router-dom";
import HistoryScrollable from "../components/HistoryScrollable";
import "./HistoryPage.css";

const HistoryPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="history-page">
      <button className="back-button" onClick={() => navigate("/")}>
        Home
      </button>
      <h1>History</h1>
      <HistoryScrollable />
    </div>
  );
};

export default HistoryPage;
