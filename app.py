from flask import Flask, render_template, request, redirect, session, url_for
import os
import hashlib
from mysql.connector import pooling
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'troque-esta-chave-no-env')

# ─── Pool de conexões ────────────────────────────────────────────────────────

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

# ─── Helpers de senha ────────────────────────────────────────────────────────

def hash_senha(senha):
    """Retorna o SHA-256 da senha em hexadecimal."""
    return hashlib.sha256(senha.encode()).hexdigest()

# ─── Seed de usuários iniciais ───────────────────────────────────────────────

def criar_usuario(usuario, senha, perfil):
    """
    Insere um usuário no banco com o perfil indicado, caso ele ainda não exista.
    Usado para popular o admin e o usuário comum a partir do .env.
    """
    if not usuario or not senha:
        print(f"[AVISO] Variáveis para o usuário '{perfil}' não definidas no .env — nenhum usuário criado.")
        return

    conexao   = get_connection()
    my_cursor = conexao.cursor()

    try:
        my_cursor.execute("SELECT id_usu FROM usuarios WHERE usuario_usu = %s", (usuario,))
        if my_cursor.fetchone():
            print(f"[INFO] Usuário '{usuario}' já existe — nenhuma alteração feita.")
            return

        my_cursor.execute(
            "INSERT INTO usuarios (usuario_usu, senha_usu, perfil_usu) VALUES (%s, %s, %s)",
            (usuario, hash_senha(senha), perfil)
        )
        conexao.commit()
        print(f"[INFO] Usuário '{usuario}' ({perfil}) criado com sucesso.")

    except Exception as e:
        conexao.rollback()
        print(f"[ERRO] Falha ao criar usuário '{usuario}': {e}")

    finally:
        my_cursor.close()
        conexao.close()


def criar_usuarios_iniciais():
    """Lê as credenciais do admin e do usuário comum a partir do .env e os cria, se necessário."""
    criar_usuario(
        os.getenv('ADMIN_USUARIO'),
        os.getenv('ADMIN_SENHA'),
        'admin'
    )
    criar_usuario(
        os.getenv('USUARIO_COMUM_USUARIO'),
        os.getenv('USUARIO_COMUM_SENHA'),
        'usuario'
    )

criar_usuarios_iniciais()


# ─── Decoradores de acesso ───────────────────────────────────────────────────

def login_required(f):
    """Bloqueia rotas para quem não está logado."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Bloqueia rotas para quem não é admin."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        if session.get('perfil') != 'admin':
            return render_template('acesso_negado.html'), 403
        return f(*args, **kwargs)
    return decorated

# ─── Autenticação ────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Já logado → vai para home
    if 'usuario_id' in session:
        return redirect(url_for('index'))

    erro = None

    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha   = request.form['senha']

        conexao   = get_connection()
        my_cursor = conexao.cursor(dictionary=True)

        try:
            my_cursor.execute(
                "SELECT * FROM usuarios WHERE usuario_usu = %s AND senha_usu = %s",
                (usuario, hash_senha(senha))
            )
            user = my_cursor.fetchone()

            if user:
                session['usuario_id'] = user['id_usu']
                session['usuario']    = user['usuario_usu']
                session['perfil']     = user['perfil_usu']   # 'admin' ou 'usuario'
                return redirect(url_for('index'))
            else:
                erro = 'Usuário ou senha incorretos.'

        finally:
            my_cursor.close()
            conexao.close()

    return render_template('login.html', erro=erro)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── Home ────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET'])
@login_required
def index():
    conexao = get_connection()
    cursor  = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM avisos")
        avisos = cursor.fetchall()

        cursor.execute("SELECT * FROM agradecimentos")
        agradecimentos = cursor.fetchall()

        cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()

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

# ─── Agradecimentos ──────────────────────────────────────────────────────────

@app.route('/agradecimentos', methods=['POST', 'GET'])
@login_required
def gracas():

    if request.method == 'POST':
        if session.get('perfil') != 'admin':
            return render_template('acesso_negado.html'), 403

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

    editando = request.args.get('editar', type=int)

    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM agradecimentos")
        result = my_cursor.fetchall()
        return render_template('agradecimentos.html', agradecimentos=result, editando=editando)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/agradecimentos/editar/<int:id>', methods=['POST'])
@admin_required
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

@app.route('/agradecimentos/confirmar-deletar/<int:id>', methods=['GET'])
@admin_required
def confirmar_deletar_agradecimento(id):
    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM agradecimentos WHERE id_agr = %s", (id,))
        item = my_cursor.fetchone()

        if not item:
            return redirect('/agradecimentos')

        return render_template('confirmar_deletar.html',
            titulo='Culto em Ação de Graça',
            campos=[('Nome', item['nome_agr']), ('Motivo', item['motivo_agr']), ('Data', item['data_agr'])],
            rota_confirmar=f'/agradecimentos/deletar/{id}',
            rota_cancelar='/agradecimentos'
        )

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/agradecimentos/deletar/<int:id>', methods=['POST'])
@admin_required
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

# ─── Avisos ──────────────────────────────────────────────────────────────────

@app.route('/avisos', methods=['POST', 'GET'])
@login_required
def avisos():

    if request.method == 'POST':
        if session.get('perfil') != 'admin':
            return render_template('acesso_negado.html'), 403

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

    editando = request.args.get('editar', type=int)

    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM avisos")
        result = my_cursor.fetchall()
        return render_template('avisos.html', avisos=result, editando=editando)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/avisos/editar/<int:id>', methods=['POST'])
@admin_required
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

@app.route('/avisos/confirmar-deletar/<int:id>', methods=['GET'])
@admin_required
def confirmar_deletar_avisos(id):
    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM avisos WHERE id_avi = %s", (id,))
        item = my_cursor.fetchone()

        if not item:
            return redirect('/avisos')

        return render_template('confirmar_deletar.html',
            titulo='Aviso',
            campos=[('Título', item['titulo_avi']), ('Descrição', item['descricao_avi']), ('Data', item['data_avi'])],
            rota_confirmar=f'/avisos/deletar/{id}',
            rota_cancelar='/avisos'
        )

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/avisos/deletar/<int:id>', methods=['POST'])
@admin_required
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

# ─── Pedidos ─────────────────────────────────────────────────────────────────

@app.route('/pedidos', methods=['POST', 'GET'])
@login_required
def pedidos():

    if request.method == 'POST':
        if session.get('perfil') != 'admin':
            return render_template('acesso_negado.html'), 403

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

    editando = request.args.get('editar', type=int)

    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM pedidos")
        result = my_cursor.fetchall()
        return render_template('pedidos.html', pedidos=result, editando=editando)

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/pedidos/editar/<int:id>', methods=['POST'])
@admin_required
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

@app.route('/pedidos/confirmar-deletar/<int:id>', methods=['GET'])
@admin_required
def confirmar_deletar_pedidos(id):
    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM pedidos WHERE id_ped = %s", (id,))
        item = my_cursor.fetchone()

        if not item:
            return redirect('/pedidos')

        return render_template('confirmar_deletar.html',
            titulo='Pedido de Oração',
            campos=[('Nome', item['nome_ped']), ('Pedido', item['motivo_ped']), ('Data', item['data_ped'])],
            rota_confirmar=f'/pedidos/deletar/{id}',
            rota_cancelar='/pedidos'
        )

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/pedidos/deletar/<int:id>', methods=['POST'])
@admin_required
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

# ─── Visitantes ──────────────────────────────────────────────────────────────

@app.route('/visitantes', methods=['POST', 'GET'])
@login_required
def visitantes():

    if request.method == 'POST':
        if session.get('perfil') != 'admin':
            return render_template('acesso_negado.html'), 403

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


    editando = request.args.get('editar', type=int)

    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)
    
    try:
        my_cursor.execute("SELECT * FROM visitantes")
        result = my_cursor.fetchall()
        return render_template('visitantes.html', visitantes=result, editando=editando)
    
    finally:
        my_cursor.close()
        conexao.close()

@app.route('/visitantes/editar/<int:id>', methods=['POST'])
@admin_required
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

@app.route('/visitantes/confirmar-deletar/<int:id>', methods=['GET'])
@admin_required
def confirmar_deletar_visitantes(id):
    conexao = get_connection()
    my_cursor = conexao.cursor(dictionary=True)

    try:
        my_cursor.execute("SELECT * FROM visitantes WHERE id_vis = %s", (id,))
        item = my_cursor.fetchone()

        if not item:
            return redirect('/visitantes')

        return render_template('confirmar_deletar.html',
            titulo='Visitante',
            campos=[('Nome', item['nome_vis']), ('Sobre', item['descricao_vis']), ('Data', item['data_vis'])],
            rota_confirmar=f'/visitantes/deletar/{id}',
            rota_cancelar='/visitantes'
        )

    finally:
        my_cursor.close()
        conexao.close()

@app.route('/visitantes/deletar/<int:id>', methods=['POST'])
@admin_required
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