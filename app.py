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
    pool_size=10,
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
    cursor = conexao.cursor(dictionary=True)

    try:
        # Buscar avisos
        cursor.execute("SELECT * FROM avisos")
        avisos = cursor.fetchall()

        # Buscar agradecimentos
        cursor.execute("SELECT * FROM agradecimentos")
        agradecimentos = cursor.fetchall()

        # Buscar pedidos
        cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()

        # Buscar visitantes
        cursor.execute("SELECT * FROM visitantes")
        visitantes = cursor.fetchall()

        return render_template(
            'index.html',
            avisos=avisos,
            agradecimentos=agradecimentos,
            pedidos=pedidos,
            visitantes=visitantes
        )

    finally:
        cursor.close()
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
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM agradecimentos")
        result = my_cursor.fetchall()
        return render_template('agradecimentos.html', agradecimentos=result)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/agradecimentos/editar/<int:id>', methods=['POST'])
def editar_agradecimento(id):   
    nome = request.form['nome']
    motivo = request.form['motivo']

    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("UPDATE agradecimentos SET nome_agr = %s, motivo_agr = %s WHERE id_agr = %s", (nome, motivo, id))
        conexao.commit()
    
    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou editar: {e}"

    finally:
        my_cursor.close()
        conexao.close()

    return redirect('/agradecimentos')

@app.route('/agradecimentos/deletar/<int:id>', methods=['POST'])
def deletar_agradecimento(id):
    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("DELETE FROM agradecimentos WHERE id_agr = %s", (id,))
        conexao.commit()
    
    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou deletar: {e}"

    finally:
        my_cursor.close()
        conexao.close()

    return redirect('/agradecimentos') 

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
        
        finally:
            my_cursor.close()
            conexao.close()

    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM avisos")
        result = my_cursor.fetchall()
        return render_template('avisos.html', avisos=result)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/avisos/editar/<int:id>', methods=['POST'])
def editar_avisos(id):  
    titulo = request.form['titulo']
    descricao = request.form['descricao']

    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("UPDATE avisos SET titulo_avi = %s, descricao_avi = %s WHERE id_avi = %s", (titulo, descricao, id))
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou editar: {e}"
    
    finally:
        my_cursor.close()
        conexao.close()
    
    return redirect('/avisos')

@app.route('/avisos/deletar/<int:id>', methods=['POST'])
def deletar_avisos(id):
    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("DELETE FROM avisos WHERE id_avi = %s", (id,))
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou deletar: {e}"
    
    finally:
        my_cursor.close()
        conexao.close()

    return redirect('/avisos')

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
        
        finally:
            my_cursor.close()
            conexao.close()

    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM pedidos")
        result = my_cursor.fetchall()
        return render_template('pedidos.html', pedidos=result)

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/pedidos/editar/<int:id>', methods=['POST'])
def editar_pedidos(id):
    nome = request.form['nome']
    motivo = request.form['motivo']

    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("UPDATE pedidos SET nome_ped = %s, motivo_ped = %s WHERE id_ped = %s", (nome, motivo, id))
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou editar: {e}"
    
    finally:
        my_cursor.close()
        conexao.close()
    
    return redirect('/pedidos')

@app.route('/pedidos/deletar/<int:id>', methods=['POST'])
def deletar_pedidos(id):
    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("DELETE FROM pedidos WHERE id_ped = %s", (id,))
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou deletar: {e}"
    
    finally:
        my_cursor.close()
        conexao.close()

    return redirect('/pedidos')

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
        
        finally:
            my_cursor.close()
            conexao.close()


    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)
    
    try:
        my_cursor.execute("SELECT * FROM visitantes")
        result = my_cursor.fetchall()
        return render_template('visitantes.html', visitantes=result)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/visitantes/editar/<int:id>', methods=['POST'])
def editar_visitantes(id):
    nome = request.form['nome']
    descricao = request.form['descricao']

    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("UPDATE visitantes SET nome_vis = %s, descricao_vis = %s WHERE id_vis = %s", (nome, descricao, id))
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou editar: {e}"
    
    finally:
        my_cursor.close()
        conexao.close()
    
    return redirect('/visitantes')

@app.route('/visitantes/deletar/<int:id>', methods=['POST'])
def deletar_visitantes(id):
    conexao = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("DELETE FROM visitantes WHERE id_vis = %s", (id,))
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        return f"Erro ao conectar ou deletar: {e}"
    
    finally:
        my_cursor.close()
        conexao.close()

    return redirect('/visitantes')

if __name__ == '__main__':
    app.run(debug=True)