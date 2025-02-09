import React from 'react';
import styled from 'styled-components';
import { Button } from '../components/Button';

const HomeContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  gap: 2rem;
`;

const Greeting = styled.h1`
  color: #333;
  font-size: 2.5rem;
  text-align: center;
  margin: 0;
`;

export const HomePage: React.FC = () => {
  return (
    <HomeContainer>
      <Greeting>Welcome to Our Amazing App!</Greeting>
      <Button to="/App.tsx">Go to App</Button>
    </HomeContainer>
  );
};
