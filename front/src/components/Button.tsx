import React from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

interface ButtonProps {
  to?: string;
  onClick?: () => void;
  children: React.ReactNode;
}

const StyledButton = styled.button`
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #45a049;
  }
`;

export const Button: React.FC<ButtonProps> = ({ to, onClick, children }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    if (to) {
      navigate(to);
    }
    onClick?.();
  };

  return <StyledButton onClick={handleClick}>{children}</StyledButton>;
};
