<h1 align="center">Missoo — Sistema de Gestão para Igrejas</h1>

<p align="center">
  Uma aplicação web desenvolvida em Python + Flask para facilitar a gestão de avisos, agradecimentos, pedidos de oração e visitantes de comunidades religiosas.
</p>

---

## Descrição do Sistema

O **Missao** é um sistema web criado para atender a uma demanda real de uma comunidade religiosa, centralizando o registro e exibição de informações como:

- **Avisos** internos da comunidade
- **Agradecimentos** enviados pelos membros
- **Pedidos de oração** cadastrados pelos participantes
- **Visitantes** recebidos nas reuniões

O projeto também tem como objetivo o desenvolvimento de competências práticas adquiridas em atividades universitárias, unindo aprendizado técnico com aplicação real.

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| **Front-end** | HTML5, Tailwind CSS, Jinja2 (templates) |
| **Back-end** | Python 3.10, Flask 3.1.3 |
| **Banco de Dados** | MySQL 8.0 |
| **Containerização** | Docker, Docker Compose |
| **Variáveis de Ambiente** | python-dotenv |

---

## Funcionalidades Principais

- **Avisos** — Cadastro e listagem de avisos da comunidade
- **Agradecimentos** — Envio de agradecimentos
- **Pedidos de Oração** — Cadastro e visualização dos pedidos
- **Visitantes** — Registro de visitantes que participaram das reuniões
- **Painel Principal** — Dashboard unificado com todos os dados em uma única tela
- **Deploy com Docker** — Ambiente totalmente containerizado para fácil implantação

---

## Prints das Telas

<p align="start">
  <img src="./static/prints/index.png" width="400">
  <img src="./static/prints/avisos.png" width="400">
  <img src="./static/prints/indexmobile.png" width="200">
  <img src="./static/prints/visitantesmobile.png" width="200">
</p>

---

## Estrutura de Pastas

```
Missao/
├── 📁 static
│   ├── 📁 prints
│   │   ├── 🖼️ avisos.png
│   │   ├── 🖼️ index.png
│   │   ├── 🖼️ indexmobile.png
│   │   └── 🖼️ visitantesmobile.png
│   └── 🎨 style.css
├── 📁 templates
│   ├── 🌐 agradecimentos.html
│   ├── 🌐 avisos.html
│   ├── 🌐 base.html
│   ├── 🌐 index.html
│   ├── 🌐 pedidos.html
│   └── 🌐 visitantes.html
├── ⚙️ .gitignore
├── 🐳 Dockerfile
├── 📝 GUIA_USUARIO.md
├── 📝 README.md
├── 🐍 app.py
├── ⚙️ docker-compose.yaml
├── 📄 requirements.txt
└── 📄 script.sql
```

---

## Como Instalar o Projeto (sem Docker)

### Pré-requisitos

- Python 3.10+
- MySQL rodando localmente
- Git

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SamuelMartins00/Missao.git
cd Missao

# 2. Crie e ative o ambiente virtual
python3 -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\Activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o banco de dados
# Acesse o MySQL e execute o script:
mysql -u root -p < script.sql

# 5. Configure o arquivo .env (veja a seção abaixo)

# 6. Rode a aplicação
flask run
```

---

## Como Configurar o `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
MYSQL_ROOT_PASSWORD= sua_senha_root
DB_HOST= localhost
DB_USER= seu_usuario
DB_PASSWORD= sua_senha
DB_NAME= igreja_db
```

> **Nunca comite o arquivo `.env` no repositório.** Ele já está listado no `.gitignore`.

| Variável | Descrição | Exemplo |
|---|---|---|
| `DB_HOST` | Host do banco de dados | `localhost` ou `db` (Docker) |
| `DB_USER` | Usuário do MySQL | `cooperador` |
| `DB_PASSWORD` | Senha do usuário MySQL | `cooperador123` |
| `DB_NAME` | Nome do banco de dados | `igreja_db` |

---

## Como Rodar com Docker

### Pré-requisitos

```bash
# 1. Atualize os pacotes do sistema
sudo apt update

# 2. Instale o Docker
sudo curl -fsSL https://get.docker.com/ | sh

# 3. Verifique a instalação
sudo docker --version

# 4. (Opcional) Use Docker sem sudo — deslogue e logue novamente após o comando
sudo usermod -aG docker $USER

# 5. Instale o Docker Compose
sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

# 6. Verifique
docker-compose --version
```

### Subindo a aplicação

```bash
# Clone o repositório
git clone https://github.com/SamuelMartins00/Missao.git
cd Missao

# Suba os containers (web + banco de dados)
docker-compose up -d

# Verifique se os containers estão rodando
docker ps

# Para derrubar a aplicação
docker-compose down
```

> O `docker-compose.yaml` já orquestra o banco MySQL e a aplicação Flask automaticamente. O banco é inicializado com o `script.sql` na primeira execução.

---

## Como Acessar o Sistema

Após subir a aplicação (com ou sem Docker), acesse pelo navegador:

| Rota | Descrição |
|---|---|
| `http://localhost:5000/` | Painel principal (dashboard) |
| `http://localhost:5000/avisos` | Gerenciar avisos |
| `http://localhost:5000/agradecimentos` | Gerenciar agradecimentos |
| `http://localhost:5000/pedidos` | Gerenciar pedidos de oração |
| `http://localhost:5000/visitantes` | Gerenciar visitantes |
