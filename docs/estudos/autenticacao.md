# Resumo sobre Autenticação

## O que é Autenticação?

Autenticação é o processo de **verificar e confirmar a identidade** de um usuário ou sistema que tenta acessar um recurso protegido, como uma conta, uma rede ou um serviço. É um componente essencial da segurança da informação, atuando como a **primeira barreira de proteção** contra acessos não autorizados.

---

## Por que a Autenticação é Importante?

A autenticação desempenha um papel crítico na segurança digital moderna, pois:

- **Garante que apenas usuários legítimos** tenham acesso a informações e recursos.
- **Ajuda a evitar violações de dados**, fraudes e roubo de identidade.
- **Suporta o cumprimento de normas e regulamentos** de segurança e privacidade.
- Estabelece uma **base confiável** para outras práticas de segurança, como a autorização e o controle de acesso.

---

## Métodos de Autenticação

### 1. Autenticação por Senha (Single-Factor Authentication - SFA)

Método mais comum e básico, onde o usuário fornece um identificador (nome de usuário ou e-mail) e uma **senha secreta**. Se os dados coincidirem com os armazenados no sistema, o acesso é concedido.

- **Vantagem**: Simples e fácil de implementar.
- **Desvantagem**: Vulnerável a ataques como **phishing**, vazamento de senhas e força bruta.

---

### 2. Autenticação de Dois Fatores (2FA - Two-Factor Authentication)

Exige que o usuário forneça **dois tipos diferentes de autenticação**, combinando:

- Algo que você **sabe** (senha)
- Algo que você **tem** (celular, token, código via app)
- Algo que você **é** (biometria)

Exemplo: após inserir a senha, o sistema envia um código por SMS ou app autenticador para confirmação.

- **Vantagem**: Muito mais seguro do que apenas senhas.
- **Desvantagem**: Requer um segundo fator (dispositivo ou app), o que pode gerar atrito na experiência do usuário.

---

### 3. Autenticação Multifator (MFA - Multi-Factor Authentication)

Expande o conceito da 2FA, exigindo **três ou mais fatores**. Por exemplo: senha + impressão digital + código temporário.

- **Vantagem**: Nível de segurança extremamente alto.
- **Desvantagem**: Mais complexa e custosa de implementar.

---

### 4. Autenticação por Certificado Digital

Utiliza **criptografia de chave pública (PKI)** para autenticar usuários e dispositivos. Um certificado digital instalado no dispositivo é usado como comprovação de identidade.

- **Usado em**: redes corporativas, VPNs, autenticação máquina a máquina.
- **Vantagem**: Alta segurança e conveniência.
- **Desvantagem**: Configuração e gerenciamento mais complexos.

---

### 5. Autenticação Biométrica

Baseada em **características físicas únicas**, como:

- Impressão digital
- Reconhecimento facial
- Reconhecimento de voz
- Leitura da íris ou retina

- **Vantagem**: Conveniente e difícil de falsificar.
- **Desvantagem**: Pode falhar em certas condições (ambiente, qualidade dos sensores) e **biometria comprometida não pode ser alterada**.

---

### 6. Autenticação Comportamental ou Baseada em Risco

Leva em conta **o contexto e o comportamento do usuário**, como:

- Localização geográfica
- Dispositivo usado
- Hora do acesso
- Padrões de uso

Quando detectado comportamento anômalo, pode solicitar autenticação adicional ou bloquear o acesso.

- **Vantagem**: Adapta-se dinamicamente ao risco.
- **Desvantagem**: Pode gerar falsos positivos e impactar a experiência.

---

## Conceitos Relacionados

- **Autorização**: Determina o que um usuário pode fazer após ser autenticado.
- **Identidade digital**: Conjunto de atributos e credenciais que representam uma entidade no meio digital.
- **IAM (Identity and Access Management)**: Conjunto de políticas e tecnologias para gerenciar identidades e acessos com segurança.

---

> Referências:
> - [Microsoft - O que é autenticação?](https://www.microsoft.com/pt-br/security/business/security-101/what-is-authentication)
> - [Cloudflare - O que é autenticação?](https://www.cloudflare.com/pt-br/learning/access-management/what-is-authentication/)
