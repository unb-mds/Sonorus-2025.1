describe('Fluxo de autenticação por voz', () => {
  it('Cadastro + login + autenticação por voz', () => {
    cy.visit('http://localhost:3000/register');
    cy.url().should('include', '/register');

    cy.get('input[placeholder="Nome"]').should('be.visible').type('Teste');
    cy.get('input[placeholder="Sobrenome"]').should('be.visible').type('Usuario');


    cy.get('input[placeholder="Seu melhor e-mail"]', { timeout: 10000 })
      .should('be.visible')
      .type('teste@gmail.com');

    cy.get('input[placeholder="Senha"]').should('be.visible').type('123456');
    cy.get('input[placeholder="Confirme a senha"]').should('be.visible').type('123456');

    cy.get('button[type="submit"]').should('not.be.disabled').click();

    cy.url().should('include', '/login');

    cy.visit('http://localhost:3000/login');
    cy.url().should('include', '/login');

    cy.get('input[placeholder="Email"]').should('be.visible').type('teste@gmail.com');
    cy.get('input[placeholder="Senha"]').should('be.visible').type('123456');
    cy.get('button[type="submit"]').should('be.visible').click();

    cy.url().should('include', '/voice-auth');
    cy.get('button#gravar').should('be.visible').click();

    cy.contains('Autenticação bem-sucedida', { timeout: 15000 }).should('be.visible');
  });
});