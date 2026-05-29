# Missao

## Descrição do sistema
O sistema Missao foi desenvolvido com dois principais objetivos: 
* desenvolver habilidades requeridas em atividades universitárias
* atender a uma demanda real de um cliente

## Tecnologias utilizadas
- Front-end:
  * HTML5
  * Tailwind
- Back-end:
  * MySQL
  * Python
    - Jinja
    - Flask

## Funcionalidades principais
- Armazenamento de dados
- Exibição dos dados

## Prints

## Estrutura das pastas 
Missao/
|
|-- static/
|    |-- style.css
|
|-- templates/
|    |-- agradecimentos.html
|    |-- avisos.html
|    |-- base.html
|    |-- index.html
|    |-- pedidos.html
|    |-- visitantes.html
|
|-- .gitignore
|
|-- Dockerfile
|
|-- README.md
|
|-- app.py
|
|-- docker-compose.yaml
|
|-- requirements.txt
|
|--script.sql


## Guia de instalção
  No terminal:
  - python3 -m venv venv 
  - . venv/Scripts/Activate
  -  - ambiente vitual ativado (venv"verde")
  - pip install -r requirements.txt

## Guia de instalação usando Docker
  No terminal linux:
  - sudo apt update --> atualiza todos os repositórios (padrão)
  - sudo curl -fsSL https://get.docker.com/ | sh --> instalando o docker
  - sudo docker --version --> verifica a instalação
  - sudo usermod -aG docker $USER --> Para usar o docker sem "sudo" use o comando abaixo, após isso deslogue e logue novamente do terminal
  - sudo curl -SL https://github.com/docker/compose/releases/download/v5.1.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose --> intalando o docker-compose
  - sudo chmod +x /usr/local/bin/docker-compose --> dando a permissão para execução
  - docker-compose --version --> verifica a instalação
  - git clone https://github.com/SamuelMartins00/Missao.git --> clona o repositório
  - cd Missao --> entra no repositório
  - docker-compose up -d --> acessado
  - docker-compose down --> derruba a aplicação 
