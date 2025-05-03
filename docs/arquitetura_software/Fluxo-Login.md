## 🔐 Fluxo de Autenticação por Biometria de Voz

### 📌 Descrição Geral

Este fluxo descreve o processo completo de login com verificação biométrica por voz, integrando a autenticação tradicional (usuário e senha) com a validação vocal. O objetivo é garantir uma autenticação segura em duas etapas, utilizando as informações biométricas previamente cadastradas.

---

### 🔄 Sequência de Ações

1. **Entrada de Credenciais**
   - O usuário digita **login e senha** no front-end (interface web).

2. **Requisição ao Back-End**
   - O front-end realiza uma **requisição HTTP (ex: POST /login)** para o back-end com os dados inseridos.

3. **Validação Inicial**
   - O back-end **valida as credenciais** recebidas e **consulta a base de dados** na tabela de usuários.

4. **Retorno da Frase de Autenticação**
   - Se a autenticação for bem-sucedida:
     - O back-end responde ao front-end com a **frase de autenticação previamente cadastrada** para aquele usuário.

5. **Autenticação Biométrica (Voz)**
   - **5.1** O front-end **capta a voz do usuário** repetindo a frase recebida.
   - **5.2** O front-end envia o **áudio gravado** para o back-end.
   - **5.3** O back-end processa a gravação e **compara os padrões biométricos de voz** com os armazenados no banco de dados.
     - O sistema permite até **3 tentativas** de validação biométrica.
   - **5.4** O back-end responde se o **login biométrico foi aprovado ou rejeitado**.
   - **5.5** O front-end exibe o **resultado final da autenticação** para o usuário.

---

### ✅ Observações Técnicas

- A comunicação entre front-end e back-end deve ser feita via **API REST segura (HTTPS)**.
- A frase usada para autenticação biométrica deve ser **individual por usuário** e armazenada com segurança.
- O áudio deve ser analisado com uma **biblioteca de processamento de sinais**, como `webrtcvad` ou `librosa`, e os dados comparados com os **vetores biométricos salvos no banco**.
- O back-end deve controlar as tentativas e aplicar política de bloqueio após 3 falhas consecutivas.

---
