from flask import Flask, render_template, request
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexão com o banco de dados
conexao = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

my_cursor = conexao.cursor()

@app.route('/', methods=['GET'])
def index():

    my_cursor = conexao.cursor()
    my_cursor.execute("SELECT * FROM avisos")
    result = my_cursor.fetchall()

    return render_template('index.html', avisos=avisos)

@app.route('/agradecimentos', methods=['POST', 'GET'])
def gracas():

    if request.method == 'POST':
        nome = request.form['titulo']
        motivo = request.form['motivo']

        try:
            my_cursor = conexao.cursor()
            comando = ("INSERT INTO agradecimentos (titulo_agr, motivo_agr) VALUES (%s, %s)")
            valores = (nome, motivo)

            my_cursor.execute(comando, valores)
            my_cursor.commit()

            return "Culto em ação de graça enviado com sucesso !"
        
        except Exception as e:
            return f"Erro ao conectar ou enviar: {e}"

    my_cursor = conexao.cursor()
    my_cursor.execute("SELECT * FROM agradecimentos")
    result = my_cursor.fetchall()

    return render_template('agradecimentos.html', agradecimentos=agradecimentos)

@app.route('/avisos', methods=['POST', 'GET'])
def avisos():

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        try:
            my_cursor = conexao.cursor()
            comando = ("INSERT INTO avisos (titulo_avi, descricao_avi) VALUES (%s, %s)")
            valores = (titulo, descricao)

            my_cursor.execute(comando, valores)
            my_cursor.commit()

            return "Aviso enviado com sucesso !"
        
        except Exception as e:
            return f"Erro ao conectar ou enviar: {e}"

    my_cursor = conexao.cursor()
    my_cursor.execute("SELECT * FROM avisos")
    result = my_cursor.fetchall()

    return render_template('avisos.html', avisos=avisos)

@app.route('/pedidos', methods=['POST', 'GET'])
def pedidos():

    if request.method == 'POST':
        nome = request.form['nome']
        pedido = request.form['motivo']

        try:
            my_cursor = conexao.cursor()
            comando = ("INSERT INTO pedidos (nome_ped, motivo_ped) VALUES (%s, %s)")
            valores = (nome, pedido)

            my_cursor.execute(comando, valores)
            my_cursor.commit()

            return "Pedido enviado com sucesso !"

        except Exception as e:
            return f"Erro ao conectar ou enviar: {e}"

    my_cursor = conexao.cursor()
    my_cursor.execute("SELECT * FROM pedidos")
    result = my_cursor.fetchall()

    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/visitantes', methods=['POST', 'GET'])
def visitantes():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        try:
            my_cursor = conexao.cursor()
            comando = ("INSERT INTO visitantes (nome_vis, descricao_vis) VALUES (%s, %s)")
            valores = (nome, descricao)

            my_cursor.execute(comando, valores)
            my_cursor.commit()

            return "Visitante avisado com sucesso !"

        except Exception as e:
            return f"Erro ao conectar ou enviar: {e}"

    my_cursor = conexao.cursor()
    my_cursor.execute("SELECT * FROM visitantes")
    result = my_cursor.fetchall()

    return render_template('visitantes.html', visitantes=visitantes)

my_cursor.close()
conexao.close()