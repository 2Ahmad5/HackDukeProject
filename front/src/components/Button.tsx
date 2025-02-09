import { useNavigate } from "react-router-dom";
import "./Button.css";

interface ButtonProps {
  to: string;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ to, children }) => {
  const navigate = useNavigate();

  return (
    <button className="styled-button" onClick={() => navigate(to)}>
      {children}
    </button>
  );
};
