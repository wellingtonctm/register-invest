import app
from Models.Usuario import Usuario
from flask import render_template, request, session, redirect, url_for

def login():
    if request.method == 'POST':
        try:
            if request.form['email'] == None or request.form['email'].strip() == '':
                raise Exception('E-mail não informado!')
            
            if request.form['senha'] == None or request.form['senha'] == '':
                raise Exception('Senha inválida!')
            
            usuario = Usuario.query.filter(Usuario.email == request.form['email'], Usuario.senha == request.form['senha']).first()
            
            if usuario == None:
                raise Exception("Usuário ou senha inválidos!");
            
            session['usuario'] = request.form['email']
            return redirect(url_for('Ativo.getAll'))
        except Exception as ex:
            return render_template('Usuario/Login.html', erro = ex)
    else:
        return render_template('Usuario/Login.html')
    
def logout():
    session.pop('usuario', None)
    return redirect(url_for('Usuarios.login'))

def getAll():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('Usuarios.login'))
    
    erro = request.args['erro'] if 'erro' in request.args else None
    usuarios = []
    
    try:
        usuarios = app.db.session.query(Usuario).order_by(Usuario.email).all()
    except Exception as ex:
        erro = ex
        
    return render_template('Usuario/Listar.html', erro = erro, usuarios = usuarios)

def create():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('Usuarios.login'))
    
    erro = None
    
    try:
        if request.form['nome'] == None or request.form['nome'].strip() == '':
            raise Exception('Nome não informado!')
        
        if request.form['email'] == None or request.form['email'].strip() == '':
            raise Exception('E-mail não informado!')
        
        if request.form['senha'] == None or len(request.form['senha']) < 8:
            raise Exception('Senha inválida!')
        
        usuario = Usuario()
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        
        app.db.session.add(usuario)
        app.db.session.commit()
    except Exception as ex:
        erro = ex
        
    return redirect(url_for('UsuarioRoute.getAll', erro=erro))


def delete():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('Usuarios.login'))
    
    erro = None
    usuarios = []
    
    try:
        if request.form['id'] == None or request.form['id'].strip() == '':
            raise Exception('Id não informado!')
        
        usuario = app.db.session.query(Usuario).get(request.form['id'])
        
        if usuario == None:
            raise Exception('Usuário não encontrado!')
        
        app.db.session.delete(usuario)
        app.db.session.commit()
        
        usuarios = app.db.session.query(Usuario).order_by(Usuario.email).all()
    except Exception as ex:
        erro = ex
    
    return render_template('Usuario/Listar.html', erro = erro, usuarios = usuarios)