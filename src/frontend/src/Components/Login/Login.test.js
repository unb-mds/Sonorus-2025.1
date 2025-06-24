import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom'; 
import { BrowserRouter, MemoryRouter } from 'react-router-dom'; 
import Login from './Login'; 

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

describe('Login Component', () => {
  test('should render login form elements (heading, email, password, and login button)', () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    expect(screen.getByRole('heading', { name: /entrar/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /esqueceu sua senha/i })).toBeInTheDocument();
  });

  test('should navigate to /register when "CADASTRE-SE" button is clicked', () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    const registerButton = screen.getByRole('button', { name: /cadastre-se/i });
    fireEvent.click(registerButton);
    expect(mockedUsedNavigate).toHaveBeenCalledTimes(1);
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/register');
  });

  test('should render "Bem-vindo" heading and paragraph in the blue section', () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    expect(screen.getByRole('heading', { name: /bem-vindo/i })).toBeInTheDocument();
    expect(screen.getByText(/primeira vez\? faça seu cadastro!/i)).toBeInTheDocument();
  });

  test('should allow users to type into email and password fields', () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    const emailInput = screen.getByPlaceholderText(/email/i);
    const passwordInput = screen.getByPlaceholderText(/senha/i);

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    expect(emailInput.value).toBe('test@example.com');

    fireEvent.change(passwordInput, { target: { value: 'mysecretpassword' } });
    expect(passwordInput.value).toBe('mysecretpassword');
  });

  test('should allow login button to be clicked', () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    const loginButton = screen.getByRole('button', { name: /login/i });
    fireEvent.click(loginButton);
  });
});