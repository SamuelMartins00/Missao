from flask import Flask, render_template
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        database=os.getenv('database')
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agradecimentos')
def gracas():
    return render_template('gracas.html')

@app.route('/avisos')
def avisos():
    return render_template('avisos.html')

@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')

@app.route('/visitantes')
def visitantes():
    return render_template('visitantes.html')