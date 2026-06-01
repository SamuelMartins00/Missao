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

O arquivo `.env` guarda as informações de conexão com o banco de dados. Ele não vem junto com o projeto por segurança, então você precisa criá-lo.

1. Dentro da pasta `Missao`, crie um arquivo chamado `.env` (com o ponto no início).

   **No terminal:**
   ```bash
   # Linux / Mac
   touch .env

   # Windows (PowerShell)
   New-Item .env
   ```

   Ou simplesmente abra qualquer editor de texto (Bloco de Notas, VS Code, etc.) e salve um arquivo com o nome `.env` dentro da pasta `Missao`.

2. Edite e cole o seguinte conteúdo dentro do arquivo:
      **No terminal:**
   ```bash
   # Linux / Mac
   nano .env

   # Windows (PowerShell)
   notepad .env
   
   cole:
   
   DB_HOST=db
   DB_USER=cooperador
   DB_PASSWORD=cooperador123
   DB_NAME=igreja_db
   ```

3. Salve o arquivo.

> **Atenção:** Esses valores já estão configurados para funcionar com o Docker. Não é necessário alterar nada.

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

Você verá o painel principal do sistema com todas as informações da comunidade.

### Páginas disponíveis:

| Endereço | O que você encontra |
|---|---|
| `http://localhost:5000/` | Painel geral com todos os dados |
| `http://localhost:5000/avisos` | Avisos da comunidade |
| `http://localhost:5000/agradecimentos` | Agradecimentos enviados |
| `http://localhost:5000/pedidos` | Pedidos de oração |
| `http://localhost:5000/visitantes` | Registro de visitantes |

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
