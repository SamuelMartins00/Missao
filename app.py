from flask import Flask, render_template, request
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexão com o banco de dados
mybd = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/', methods=['GET'])
def index():

    my_cursor = mybd.cursor()
    my_cursor.execute("SELECT * FROM avisos")
    avisos = my_cursor.fetchall()

    return render_template('index.html', avisos=avisos)

@app.route('/agradecimentos', methods=['POST', 'GET'])
def gracas():

    if request.method == 'POST':
        nome = request.form['nome']
        agradecimento = request.form['motivo']

        my_cursor = mybd.cursor()
        my_cursor.execute("INSERT INTO agradecimentos (nome, agradecimento) VALUES (%s, %s)", (nome, agradecimento))
        my_cursor.commit()
        
    my_cursor = mybd.cursor()
    my_cursor.execute("SELECT * FROM agradecimentos")
    agradecimentos = my_cursor.fetchall()

    return render_template('agradecimentos.html', agradecimentos=agradecimentos)

@app.route('/avisos', methods=['POST', 'GET'])
def avisos():

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        my_cursor = mybd.cursor()
        my_cursor.execute("INSERT INTO avisos (titulo, descricao) VALUES (%s, %s)", (titulo, descricao))
        my_cursor.commit()

    my_cursor = mybd.cursor()
    my_cursor.execute("SELECT * FROM avisos")
    avisos = my_cursor.fetchall()

    return render_template('avisos.html', avisos=avisos)

@app.route('/pedidos', methods=['POST', 'GET'])
def pedidos():

    if request.method == 'POST':
        nome = request.form['nome']
        pedido = request.form['pedido']

        my_cursor = mybd.cursor()
        my_cursor.execute("INSERT INTO pedidos (nome, pedido) VALUES (%s, %s)", (nome, pedido))
        my_cursor.commit()

    my_cursor = mybd.cursor()
    my_cursor.execute("SELECT * FROM pedidos")
    pedidos = my_cursor.fetchall()

    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/visitantes', methods=['POST', 'GET'])
def visitantes():
    if request.method == 'POST':
        nome = request.form['nome']
        motivo = request.form['motivo']

        my_cursor = mybd.cursor()
        my_cursor.execute("INSERT INTO visitantes (nome, motivo) VALUES (%s, %s)", (nome, motivo))
        my_cursor.commit()

    my_cursor = mybd.cursor()
    my_cursor.execute("SELECT * FROM visitantes")
    visitantes = my_cursor.fetchall()

    return render_template('visitantes.html', visitantes=visitantes)