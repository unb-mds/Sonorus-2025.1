// src/Components/Registro/Register.test.js
// força a mesma URL de DNS que os mocks abaixo esperam:
process.env.REACT_APP_DNS_API_URL = 'https://dns.example.com/api/lookup';

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import Register from './Register';

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

global.fetch = jest.fn();

const BASE_API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');
const DNS_API_BASE_URL = process.env.REACT_APP_DNS_API_URL;
const CHECK_EMAIL_URL = `${BASE_API_URL}/check-email`;
const REGISTER_URL = `${BASE_API_URL}/registrar`;

describe('Register Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch.mockImplementation(url => {
      if (url.startsWith(DNS_API_BASE_URL)) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ Answer: [{ type: 'MX' }] }) });
      }
      if (url.startsWith(CHECK_EMAIL_URL)) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ exists: false }) });
      }
      if (url.startsWith(REGISTER_URL)) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
      }
      return Promise.reject(new Error(`Unexpected fetch: ${url}`));
    });
  });

  test('renders all form elements and toggle buttons', () => {
    render(<Register />, { wrapper: MemoryRouter });
    expect(screen.getByRole('heading', { name: /cadastre-se/i })).toBeInTheDocument();
    ['Nome','Sobrenome','Seu melhor e-mail','Senha','Confirme a senha']
      .forEach(ph => expect(screen.getByPlaceholderText(ph)).toBeInTheDocument());
    const btn = screen.getByRole('button', { name: /continuar/i });
    expect(btn).toBeDisabled();
    expect(screen.getAllByLabelText('toggle password visibility')).toHaveLength(2);
  });

  test('toggle password visibility', () => {
    render(<Register />, { wrapper: MemoryRouter });
    const pwd = screen.getByPlaceholderText('Senha');
    const pwd2 = screen.getByPlaceholderText('Confirme a senha');
    const toggles = screen.getAllByLabelText('toggle password visibility');
    fireEvent.click(toggles[0]);
    expect(pwd).toHaveAttribute('type','text');
    fireEvent.click(toggles[0]);
    expect(pwd).toHaveAttribute('type','password');
    fireEvent.click(toggles[1]);
    expect(pwd2).toHaveAttribute('type','text');
    fireEvent.click(toggles[1]);
    expect(pwd2).toHaveAttribute('type','password');
  });

  test('invalid email shows domain error and blocks submit', async () => {
    // override DNS lookup para retornar vazio
    global.fetch.mockImplementationOnce(url => {
      if (url.startsWith(DNS_API_BASE_URL)) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ Answer: [] }) });
      }
      return Promise.reject();
    });

    const { container } = render(<Register />, { wrapper: MemoryRouter });
    const emailInput = screen.getByPlaceholderText('Seu melhor e-mail');
    fireEvent.change(emailInput, { target: { value: 'test@invalido.com' } });

    await waitFor(() =>
      expect(screen.getByText('O domínio do email não existe ou não está configurado para receber emails'))
        .toBeInTheDocument()
    );

    // simula submit direto
    fireEvent.submit(container.querySelector('form'));
    await waitFor(() =>
      expect(screen.getByText('Por favor, corrija os erros no formulário')).toBeInTheDocument()
    );
  });

  test('password mismatch error', async () => {
    render(<Register />, { wrapper: MemoryRouter });
    fireEvent.change(screen.getByPlaceholderText('Nome'),{ target:{ value:'A' } });
    fireEvent.change(screen.getByPlaceholderText('Sobrenome'),{ target:{ value:'B' } });
    fireEvent.change(screen.getByPlaceholderText('Seu melhor e-mail'),{ target:{ value:'a@b.com' } });
    await waitFor(() =>
      expect(screen.getByRole('button',{ name:/continuar/i })).not.toBeDisabled()
    );
    fireEvent.change(screen.getByPlaceholderText('Senha'),{ target:{ value:'123456' } });
    fireEvent.change(screen.getByPlaceholderText('Confirme a senha'),{ target:{ value:'654321' } });
    fireEvent.click(screen.getByRole('button',{ name:/continuar/i }));
    await waitFor(() =>
      expect(screen.getByText('As senhas não coincidem')).toBeInTheDocument()
    );
  });

  test('successful registration navigates', async () => {
    render(<Register />, { wrapper: MemoryRouter });
    fireEvent.change(screen.getByPlaceholderText('Nome'),{ target:{ value:'New' } });
    fireEvent.change(screen.getByPlaceholderText('Sobrenome'),{ target:{ value:'User' } });
    fireEvent.change(screen.getByPlaceholderText('Seu melhor e-mail'),{ target:{ value:'new@ex.com' } });
    await waitFor(() =>
      expect(screen.getByRole('button',{ name:/continuar/i })).not.toBeDisabled()
    );
    fireEvent.change(screen.getByPlaceholderText('Senha'),{ target:{ value:'123456' } });
    fireEvent.change(screen.getByPlaceholderText('Confirme a senha'),{ target:{ value:'123456' } });
    fireEvent.click(screen.getByRole('button',{ name:/continuar/i }));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith('/cadastro-voz', expect.any(Object))
    );
  });

  test('API failure navigates to /erroCadastro', async () => {
    global.fetch.mockImplementation(url => {
      if (url.startsWith(DNS_API_BASE_URL)) {
        return Promise.resolve({ ok:true, json:() => Promise.resolve({ Answer:[{type:'MX'}] }) });
      }
      if (url.startsWith(CHECK_EMAIL_URL)) {
        return Promise.resolve({ ok:true, json:() => Promise.resolve({ exists:false }) });
      }
      if (url.startsWith(REGISTER_URL)) {
        return Promise.resolve({ ok:false, json:() => Promise.resolve({ detail:'fail' }) });
      }
      return Promise.reject();
    });

    render(<Register />, { wrapper: MemoryRouter });
    fireEvent.change(screen.getByPlaceholderText('Nome'),{ target:{ value:'X' } });
    fireEvent.change(screen.getByPlaceholderText('Sobrenome'),{ target:{ value:'Y' } });
    fireEvent.change(screen.getByPlaceholderText('Seu melhor e-mail'),{ target:{ value:'fail@ex.com' } });
    await waitFor(() =>
      expect(screen.getByRole('button',{ name:/continuar/i })).not.toBeDisabled()
    );
    fireEvent.change(screen.getByPlaceholderText('Senha'),{ target:{ value:'abcdef' } });
    fireEvent.change(screen.getByPlaceholderText('Confirme a senha'),{ target:{ value:'abcdef' } });
    fireEvent.click(screen.getByRole('button',{ name:/continuar/i }));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith('/erroCadastro')
    );
  });

  test('“FAÇA LOGIN” navigates to /login', () => {
    render(<Register />, { wrapper: MemoryRouter });
    fireEvent.click(screen.getByRole('button',{ name:/faça login/i }));
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/login');
  });
});
