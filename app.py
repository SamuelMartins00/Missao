from flask import Flask, render_template, request, redirect
import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexão com o banco de dados
pool = pooling.MySQLConnectionPool(
    pool_name="igreja_pool",
    pool_size=5,
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

def get_connection():
    return pool.get_connection()

@app.route('/', methods=['GET'])
def index():
    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("SELECT * FROM avisos")
        result = my_cursor.fetchall()
        return render_template('index.html', avisos=result)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/agradecimentos', methods=['POST', 'GET'])
def gracas():

    if request.method == 'POST':
        nome = request.form['nome']
        motivo = request.form['motivo']

        conexao = get_connection()
        my_cursor = conexao.cursor()

        try:
            comando = ("INSERT INTO agradecimentos (nome_agr, motivo_agr) VALUES (%s, %s)")
            valores = (nome, motivo)

            my_cursor.execute(comando, valores)
            conexao.commit()

            return redirect('/agradecimentos')
        
        except Exception as e:
            conexao.rollback()
            return f"Erro ao conectar ou enviar: {e}"
        
        finally:
            my_cursor.close()
            conexao.close() 

    conexao = get_connection()
    my_cursor = conexao.cursor()   

    try:
        my_cursor.execute("SELECT * FROM agradecimentos")
        result = my_cursor.fetchall()
        return render_template('agradecimentos.html', agradecimentos=result)
    
    finally:
        my_cursor.close()
        conexao.close()
        
@app.route('/avisos', methods=['POST', 'GET'])
def avisos():

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        conexao = get_connection()
        my_cursor = conexao.cursor()

        try:
            comando = ("INSERT INTO avisos (titulo_avi, descricao_avi) VALUES (%s, %s)")
            valores = (titulo, descricao)

            my_cursor.execute(comando, valores)
            conexao.commit()

            return redirect('/avisos')
        
        except Exception as e:
            conexao.rollback()
            return f"Erro ao conectar ou enviar: {e}"

    conexao = get_connection()
    my_cursor = conexao.cursor()
    try:
        my_cursor.execute("SELECT * FROM avisos")
        result = my_cursor.fetchall()
        return render_template('avisos.html', avisos=result)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/pedidos', methods=['POST', 'GET'])
def pedidos():

    if request.method == 'POST':
        nome = request.form['nome']
        pedido = request.form['motivo']

        conexao = get_connection()
        my_cursor = conexao.cursor()
        
        try:
            comando = ("INSERT INTO pedidos (nome_ped, motivo_ped) VALUES (%s, %s)")
            valores = (nome, pedido)

            my_cursor.execute(comando, valores)
            conexao.commit()

            return redirect('/pedidos')

        except Exception as e:
            conexao.rollback()
            return f"Erro ao conectar ou enviar: {e}"

    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("SELECT * FROM pedidos")
        result = my_cursor.fetchall()
        return render_template('pedidos.html', pedidos=result)

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/visitantes', methods=['POST', 'GET'])
def visitantes():

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        conexao = get_connection()
        my_cursor = conexao.cursor()

        try:
            comando = ("INSERT INTO visitantes (nome_vis, descricao_vis) VALUES (%s, %s)")
            valores = (nome, descricao)

            my_cursor.execute(comando, valores)
            conexao.commit()

            return redirect('/visitantes')

        except Exception as e:
            conexao.rollback()
            return f"Erro ao conectar ou enviar: {e}"

    conexao = get_connection()
    my_cursor = conexao.cursor()
    
    try:
        my_cursor.execute("SELECT * FROM visitantes")
        result = my_cursor.fetchall()
        return render_template('visitantes.html', visitantes=result)
    
    finally:
        my_cursor.close()
        conexao.close()

if __name__ == '__main__':
    app.run(debug=True)
 