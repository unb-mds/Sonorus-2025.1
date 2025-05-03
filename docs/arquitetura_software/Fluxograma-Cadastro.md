## Fluxo de Cadastro do Sistema Bancário com Biometria de Voz

Este fluxograma representa a etapa de **cadastro** do sistema bancário, com ênfase na segurança e autenticação biométrica por voz. A aplicação será desenvolvida em **Python**, com integração de **inteligência artificial** para o reconhecimento de voz, e usará o **Oracle Database** como sistema de armazenamento.

### 🧩 Etapas do Cadastro

1. **Cadastro**
   - O usuário inicia o processo de cadastro fornecendo dados básicos.

2. **Criar Usuário**
   - Os dados iniciais são utilizados para criar um registro preliminar do usuário no sistema.

3. **Confirmar E-mail**
   - É enviada uma solicitação de confirmação de e-mail para garantir a validade do endereço de contato. Após confirmação, os dados são armazenados no banco Oracle.

4. **Gerar Mensagem Aleatória**
   - O sistema, usando IA, gera uma **frase aleatória** que servirá como base para a biometria de voz.

5. **Buscar e Alocar Frase para Biometria**
   - A frase gerada é associada ao perfil do usuário.

6. **Registrar Biometria**
   - O usuário grava sua voz falando a frase alocada. Essa amostra será utilizada para autenticação futura.

7. **Cadastro Finalizado**
   - Com todos os dados gravados, incluindo a amostra de voz e senha criptografada com hash, o cadastro é finalizado e armazenado de forma segura no banco Oracle.

### 🛠️ Tecnologias Utilizadas

- **Back-end**: Python com bibliotecas de reconhecimento de voz e segurança (ex: `SpeechRecognition`, `pyttsx3`, `bcrypt`).
- **Banco de Dados**: Oracle Database, armazenando os dados dos usuários, frases aleatórias, hashes de senha e amostras biométricas.
- **IA / Machine Learning**: Treinamento e verificação das amostras de voz.

### 🔐 Segurança

- Senhas são **criptografadas com hash** antes do armazenamento.
- A autenticação futura será feita via **biometria de voz** comparando a frase falada com a amostra registrada.

---

Este processo visa oferecer **segurança reforçada** e **experiência personalizada** para cada cliente, tornando o acesso ao sistema mais confiável e moderno.
