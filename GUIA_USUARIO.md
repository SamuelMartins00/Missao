# Guia do Usuário — Sistema Missao

> Este guia foi escrito para qualquer pessoa conseguir rodar o sistema, mesmo sem conhecimento técnico em programação. Siga os passos com calma e tudo funcionará! 

---

## Pré-requisitos

Antes de começar, você precisa ter instalado no seu computador:

### 1. Git
Usado para baixar o projeto do GitHub.

- **Windows:** Acesse [https://git-scm.com/download/win](https://git-scm.com/download/win) e instale normalmente.
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update && sudo apt install git -y
  ```
- **Mac:** Acesse [https://git-scm.com/download/mac](https://git-scm.com/download/mac).

Para verificar se já está instalado, abra o terminal e digite:
```bash
git --version
```

---

### 2. Docker Desktop (Windows e Mac) ou Docker Engine (Linux)

O Docker é a única ferramenta necessária para rodar o sistema. Ele cuida de tudo — banco de dados, servidor, configurações — automaticamente.

**Windows / Mac:**
Acesse [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop), baixe e instale o **Docker Desktop**.

> No Windows, o Docker Desktop pode pedir para ativar o WSL 2. Siga as instruções que aparecerem na tela.

**Linux (Ubuntu/Debian):**
```bash
# Instala o Docker
sudo curl -fsSL https://get.docker.com/ | sh

# Instala o Docker Compose
sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

# Permite usar Docker sem "sudo" (reinicie o terminal depois)
sudo usermod -aG docker $USER
```

Para verificar se está instalado corretamente:
```bash
docker --version
docker-compose --version
```

---

## Como Baixar o Projeto

1. Abra o terminal do seu computador:
   - **Windows:** Pesquise por "Prompt de Comando" ou "PowerShell" no menu iniciar
   - **Mac:** Pesquise por "Terminal"
   - **Linux:** Atalho `Ctrl + Alt + T`

2. Escolha uma pasta onde o projeto ficará salvo. Por exemplo, a área de trabalho:
   ```bash
   # Windows
   cd Desktop

   # Linux / Mac
   cd ~/Desktop
   ```

3. Baixe o projeto com o Git:
   ```bash
   git clone https://github.com/SamuelMartins00/Missao.git
   ```

4. Entre na pasta do projeto:
   ```bash
   cd Missao
   ```

Pronto! Agora você tem todos os arquivos do sistema no seu computador.

---

## Como Configurar o Arquivo `.env`

O arquivo `.env` guarda as informações de conexão com o banco de dados **e os usuários que vão acessar o sistema**. Ele não vem junto com o projeto por segurança, então você precisa criá-lo.

1. Dentro da pasta `Missao`, crie um arquivo chamado `.env` (com o ponto no início).

   **No terminal:**
   ```bash
   # Linux / Mac
   touch .env

   # Windows (PowerShell)
   New-Item .env
   ```

   Ou simplesmente abra qualquer editor de texto (Bloco de Notas, VS Code, etc.) e salve um arquivo com o nome `.env` dentro da pasta `Missao`.

2. Edite o arquivo e cole o seguinte conteúdo dentro dele:

   **No terminal:**
   ```bash
   # Linux / Mac
   nano .env

   # Windows (PowerShell)
   notepad .env
   ```

   **Cole isto dentro do arquivo:**
   ```env
   DB_HOST=db
   DB_USER=root
   DB_PASSWORD=cooperador123
   DB_NAME=igreja_db

   MYSQL_ROOT_PASSWORD=cooperador123
   MYSQL_DATABASE=igreja_db
   MYSQL_USER=root
   MYSQL_PASSWORD=cooperador123

   SECRET_KEY=troque_por_um_codigo_aleatorio_longo

   ADMIN_USUARIO=admin
   ADMIN_SENHA=defina_uma_senha_forte

   USUARIO_COMUM_USUARIO=membro
   USUARIO_COMUM_SENHA=defina_outra_senha_forte
   ```

3. **Troque os valores de exemplo pelos seus.** O importante de entender em cada linha:

   | O que é | O que fazer |
   |---|---|
   | `ADMIN_USUARIO` / `ADMIN_SENHA` | Defina o usuário e senha de quem vai **administrar** o sistema (criar, editar e excluir registros) |
   | `USUARIO_COMUM_USUARIO` / `USUARIO_COMUM_SENHA` | Defina o usuário e senha de quem vai só **visualizar** os dados, sem poder alterar nada |
   | `SECRET_KEY` | Uma sequência de letras e números aleatória, usada internamente pelo sistema para proteger o login. Pode ser qualquer texto longo e difícil de adivinhar — não precisa anotar nem lembrar dela depois |
   | `DB_*` e `MYSQL_*` | Senhas internas do banco de dados — pode manter os valores de exemplo ou trocar, desde que `DB_PASSWORD` e `MYSQL_PASSWORD` sejam **iguais** |

   > Esses dois usuários (`admin` e o usuário comum) são criados automaticamente dentro do sistema na primeira vez que ele é iniciado. Depois disso, essas quatro linhas (`ADMIN_*` e `USUARIO_COMUM_*`) não são mais necessárias e podem até ser apagadas do `.env` — mas não tem problema se ficarem.

4. Salve o arquivo.

> **Atenção:** Guarde o usuário e a senha que você escolheu para o admin e para o usuário comum — você vai usá-los para entrar no sistema mais adiante.

---

## Como Subir os Containers (Iniciar o Sistema)

Com o Docker instalado e o arquivo `.env` criado, agora é só subir o sistema com um único comando.

Ainda dentro da pasta `Missao` no terminal, execute:

```bash
docker-compose up -d
```

O que vai acontecer:
- O Docker vai baixar as imagens necessárias (MySQL e a aplicação) — **isso pode levar alguns minutos na primeira vez**
- O banco de dados será criado e configurado automaticamente
- A aplicação será iniciada em segundo plano

Para verificar se tudo está rodando corretamente:
```bash
docker ps
```

Você verá dois containers ativos:

| Container | Descrição |
|---|---|
| `igreja_db` | Banco de dados MySQL |
| `igreja_web` | Aplicação web Flask |

> Se ambos aparecerem com status `Up`, o sistema está funcionando!

---

## Como Acessar pelo Navegador

Após subir os containers, abra qualquer navegador (Chrome, Firefox, Edge…) e acesse:

```
http://localhost:5000
```

Você será levado direto para a **tela de login**. Digite o usuário e a senha que você definiu no arquivo `.env` (`ADMIN_USUARIO`/`ADMIN_SENHA` para acesso total, ou `USUARIO_COMUM_USUARIO`/`USUARIO_COMUM_SENHA` para acesso de visualização) e clique em **Entrar**.

> Se aparecer a mensagem "Usuário ou senha incorretos", confira se digitou exatamente o que colocou no `.env` — letras maiúsculas/minúsculas fazem diferença.

### Os dois tipos de acesso

| Quem loga com... | Pode fazer |
|---|---|
| `ADMIN_USUARIO` / `ADMIN_SENHA` | Ver, **criar**, **editar** e **excluir** avisos, agradecimentos, pedidos e visitantes |
| `USUARIO_COMUM_USUARIO` / `USUARIO_COMUM_SENHA` | Apenas **ver** as informações — sem botões de criar, editar ou excluir |

Depois de logado, você verá seu nome de usuário no canto superior da tela, junto com o botão **Sair** — use-o para encerrar a sessão quando terminar de usar o sistema.

### Páginas disponíveis:

| Endereço | O que você encontra |
|---|---|
| `http://localhost:5000/` | Painel geral com todos os dados |
| `http://localhost:5000/avisos` | Avisos da comunidade |
| `http://localhost:5000/agradecimentos` | Agradecimentos enviados |
| `http://localhost:5000/pedidos` | Pedidos de oração |
| `http://localhost:5000/visitantes` | Registro de visitantes |

### Editando ou excluindo um registro (somente para admin)

- Para **editar**, clique no botão "Editar" ao lado do registro desejado, altere os campos e clique em "Salvar"
- Para **excluir**, clique em "Deletar" — o sistema vai mostrar uma tela perguntando se você tem certeza, mostrando os dados do registro antes de remover de forma definitiva

---

## Como Parar o Sistema

Quando quiser desligar o sistema, vá ao terminal, certifique-se de estar dentro da pasta `Missao` e execute:

```bash
docker-compose down
```

Isso vai parar e remover os containers. **Os dados salvos no banco de dados serão preservados** — eles ficam armazenados em um volume do Docker.

Para subir o sistema novamente no futuro, basta repetir:
```bash
docker-compose up -d
```

---

## Problemas Comuns

**"A página não carrega no navegador"**
> Aguarde cerca de 30 segundos após rodar o `docker-compose up -d`. O banco de dados precisa de um momento para inicializar antes da aplicação conectar.

**"O Docker não é reconhecido no terminal"**
> Feche e abra o terminal novamente após a instalação do Docker. No Windows, certifique-se de que o Docker Desktop está aberto e rodando (ícone na barra de tarefas).

**"Erro de permissão no Linux"**
> Execute o comando `sudo usermod -aG docker $USER`, deslogue do sistema e logue novamente. Depois tente rodar o `docker-compose up -d` sem `sudo`.

**"Usuário ou senha incorretos" na tela de login**
> Confira se digitou exatamente o usuário e a senha que você colocou em `ADMIN_USUARIO`/`ADMIN_SENHA` ou `USUARIO_COMUM_USUARIO`/`USUARIO_COMUM_SENHA` no arquivo `.env`. Se ainda não conseguir entrar, confirme que essas variáveis estavam preenchidas no `.env` **antes** da primeira vez que você rodou `docker-compose up -d` — é nesse momento que os usuários são criados.

**"Não vejo os botões de Editar e Deletar"**
> Isso é esperado se você fez login com o usuário comum (`USUARIO_COMUM_USUARIO`). Esse perfil só pode visualizar os dados. Para criar, editar ou excluir registros, faça login com o usuário administrador (`ADMIN_USUARIO`).