# Estudo sobre Git

Git é um sistema de controle de versão distribuído amplamente utilizado para gerenciar projetos de software. Ele permite que várias pessoas colaborem em um projeto, rastreando mudanças no código e facilitando o trabalho em equipe.

---

## Como funciona o Git

O Git funciona rastreando alterações em arquivos e armazenando essas alterações em um repositório. Ele utiliza três áreas principais:

1. **Working Directory**: Onde você faz alterações nos arquivos.
2. **Staging Area**: Onde você prepara as alterações para serem confirmadas.
3. **Repository**: Onde as alterações confirmadas são armazenadas.

## Como começar a desenvolver

### Clonando o repositório

Para clonar o repositório remoto na sua máquinam use o comando:

```bash
git clone https://github.com/unb-mds/2025-1-Squad05.git
```

### Criando uma branch

Sempre antes de criar uma branch é importante atualizar a branch de origem com o comando:

```bash
git pull
```

Uma branch é uma linha de desenvolvimento independente. Para criar uma branch, use o comando:

```bash
git checkout -b minha-branch
```

Isso cria e muda para a nova branch chamada minha-branch. Sempre crie uma branch para trabalhar em novas funcionalidades ou correções.

### Fazendo um commit

Um commit é como um "salvar" no Git. Ele registra as alterações feitas nos arquivos. Para fazer um commit:

1. Adicione os arquivos à staging area:

```bash
git add .
```

2. Faça o commit:

```bash
git commit -m "Descrição clara do que foi alterado"
```

### Enviando para o repositório remoto

Depois de fazer commits, envie suas alterações para o repositório remoto (GitHub):

```bash
git push origin minha-branch
```

## Pull Requests

Um Pull Request (PR) é uma solicitação para mesclar suas alterações na branch principal. Para criar um PR:

1. Envie sua branch para o repositório remoto.
2. Acesse o repositório no GitHub.
3. Clique em "Pull Requests" e depois em "New Pull Request".
4. Escolha a branch que deseja mesclar e adicione uma descrição clara.

### Avaliando um Pull Request (Code Review)

O processo de avaliação de um Pull Request (PR) é essencial para garantir a qualidade do código e a colaboração eficaz entre os membros da equipe. Aqui estão os passos e boas práticas para realizar um Code Review:

#### 1. **Entenda o Contexto**
   - Leia a descrição do PR para entender o objetivo das alterações.
   - Verifique se há links para issues ou tarefas relacionadas no Github.

#### 2. **Analise o Código**
   - **Clareza**: O código é fácil de entender? Há comentários explicativos para trechos complexos?
   - **Funcionalidade**: O código atende ao objetivo descrito no PR? Teste as alterações localmente, se necessário.
   - **Boas Práticas**: Verifique se o código segue os padrões de estilo e boas práticas definidos pela equipe.
   - **Impacto**: Avalie se as alterações podem causar problemas em outras partes do projeto.

#### 3. **Teste as Alterações**
   - Execute os testes automatizados para garantir que o código não quebre funcionalidades existentes.
   - Se possível, teste manualmente as alterações para verificar o comportamento esperado.

#### 4. **Forneça Feedback**
   - Seja claro e objetivo ao apontar problemas ou sugerir melhorias.
   - Use um tom construtivo e educado. Por exemplo:
     - ✅ "Ótimo trabalho! O código está bem organizado."
     - ⚠️ "Poderia adicionar um comentário explicando essa lógica? Ficaria mais fácil para outros entenderem."
     - ❌ "Isso está errado. Refatore."

#### 5. **Aprove ou Solicite Alterações**
   - Se o código estiver pronto para ser mesclado, aprove o PR.
   - Caso precise de ajustes, solicite alterações e explique o que precisa ser corrigido.

#### 6. **Mesclando o PR**
   - Certifique-se de que o PR foi revisado por pelo menos um outro membro da equipe.
   - Antes de mesclar, atualize a branch do PR com a branch principal para evitar conflitos:
     ```bash
     git pull origin main
     ```
   - Mescle o PR usando a interface do GitHub.

---

#### Boas Práticas para Code Review
- **Seja colaborativo**: O objetivo é melhorar o código, não criticar o autor.
- **Foque no código, não na pessoa**: Evite comentários pessoais.
- **Documente padrões e práticas**: Facilite o processo de revisão criando guias de estilo e boas práticas para o projeto.

---

#### Ferramentas Úteis
- **GitHub**: Use a aba "Files changed" para revisar as alterações diretamente no PR.

Com essas etapas, o processo de Code Review será mais eficiente e contribuirá para a qualidade do projeto.

### Resolvendo Conflitos

Conflitos acontecem quando duas pessoas fazem alterações na mesma parte do código. Para resolver:

1. O Git indicará os arquivos com conflitos.
2. Edite os arquivos para resolver os conflitos.
3. Após resolver, adicione os arquivos e faça um commit:

```bash
git add .
git commit -m "Resolvendo conflitos"
```

## Comandos Úteis

- Verificar o status do repositório:

```bash
git status
```

- Ver histórico de commits:

```bash
git log
```

- Atualizar sua branch com a branch principal:

```bash
git pull origin main
```

## Dicas e Boas Práticas

- Sempre escreva mensagens de commit claras e descritivas.
- Atualize sua branch com a branch principal antes de criar um Pull Request.
- Divida grandes alterações em commits menores e mais fáceis de entender.
- Use `.gitignore` para evitar enviar arquivos desnecessários ao repositório.

## Sugestão de conteúdo para aprofundamento

- [Minicurso de Git (45m)](https://youtu.be/ts-H3W1uLMM?si=ZcaIaaZUY6q2sQ1x)
- [Tutorial simplificado](https://rogerdudler.github.io/git-guide/index.pt_BR.html)