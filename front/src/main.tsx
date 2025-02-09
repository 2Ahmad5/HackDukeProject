import ReactDOM from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom"; // Changed to HashRouter
import App from "./App";
import { HomePage } from "./pages/HomePage";
import HistoryPage from "./pages/HistoryPage";
import "./index.css";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <HashRouter>
    {" "}
    {/* Changed from BrowserRouter */}
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/app" element={<App />} />
      <Route path="/history" element={<HistoryPage />} />
    </Routes>
  </HashRouter>
);
