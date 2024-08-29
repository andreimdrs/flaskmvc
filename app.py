from flask import Flask, url_for, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = '9t8b2489vh42v2vv'

def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    conn.row_factory = sqlite3.Row  # Opcional: permite acessar colunas pelo nome
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM usuario")
    emails = cursor.fetchall()
    return render_template('pages/index.html', emails=emails)

@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    new_email = request.form['email']
    new_password = request.form['password']
    
    # Validação simples (verifique se os campos não estão vazios, por exemplo)
    if not new_email or not new_password:
        return "Email e senha são obrigatórios.", 400

    # Atualiza o usuário no banco de dados
    cursor.execute("""
        UPDATE usuario
        SET email = ?, senha = ?
        WHERE email = ?
    """, (new_email, new_password, email))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('user_page', email=new_email))

@app.route('/user/<email>')
def user_page(email):
    if session['email'] == email:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('pages/user.html', user=user)
        else:
            return "Usuário não encontrado", 404
    else:
        return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            senha = request.form['password']
        
            # Verificando se o usuário existe no banco de dados
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE email =?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user and user['senha'] == senha:
                session['email'] = email
                session['id'] = user['id']
                return redirect(url_for('index', email=email))
        except KeyError as e:
                return "Email ou senha inválidos", 401
        finally:
            conn.close()  # Fechar a conexão
    else:
        return render_template('pages/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Obtendo dados do formulário
            email = request.form['email']
            senha = request.form['password']
            
            #conexao
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Inserindo dados na tabela
            sql = "INSERT INTO usuario (email, senha) VALUES (?, ?)"
            cursor.execute(sql, (email, senha))
            conn.commit()
            
            return redirect('/')
        except KeyError as e:
            return f"Campo ausente: {str(e)}", 400
        finally:
            conn.close()  # Fechar a conexão
    else:
        return render_template('pages/register.html')
@app.route('/cadastro_livros', methods=['POST', 'GET'])
def cadastro_livros():
    if request.method == 'POST':
        session
        # Verificando se o usuário existe no banco de dados
        # Verificando se o usuário existe no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        user = cursor.fetchone()
        conn.close()

        titulo = request.form['titulo']
        autor = request.form['autor']
        texto = request.form['texto']
        usuario_id = session.get('id') 

        # Inserindo dados na tabela
        sql = "INSERT INTO livros (titulo, autor, texto, id_usuario) VALUES (?,?,?,?)"
        cursor.execute(sql, (titulo, autor, texto, usuario_id))
        conn.commit()
        conn.close()
    else:
        return render_template('pages/cadastro_livros.html')
@app.route('/logout')
def logout():
    # Remove a informação do usuário da sessão
    session.pop('email', None)  # 'email' é a chave usada para armazenar o email do usuário
    
    # Redireciona para a página inicial ou outra página desejada
    return redirect(url_for('index'))
        
@app.route("/create_database")
def create_database():
    db = 'database.sqlite'
    schema = 'database/schema.sql'
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    with open(schema, 'r') as banco:
        schema_sql = banco.read()
        cursor.executescript(schema_sql)
    return 'BANCO CRIADO'


if __name__ == '__main__':
    app.run(debug=True)