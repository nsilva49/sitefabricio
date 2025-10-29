# todo formulário deverá ter token de segurança
# para gerar o token, vai em terminal, python(enter),
# import secrets(enter),secrets.token_hex(16), exit()
# o routes controla as páginas

from fileinput import filename
from translate import Translator
from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required# exige que faça o login para acessar a página
import secrets
import os
from PIL import Image,ImageOps


# # Lista de usuários fictícios para exibição
# lista_usuarios = ['Caio', 'Luísa', 'Vivian', 'Fabrício']

# Página inicial
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()).all() # imprime os posts em ordem decrescente
    return render_template('home.html', posts=posts)

# Página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Página de usuários
@app.route('/usuarios')
@login_required # página bloqueado. Só acessa se fizer login
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    #traduzir = Translator(from_lang='English', to_lang='pt-br')  # Tradutor de mensagens, se necessário

    # Verifica se o botão de login foi clicado e o formulário é válido
    if 'botao_submit_login' in request.form and form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert_success')
            par_next = request.args.get('next')
            return redirect(par_next or url_for('home'))
        else:
            flash('Falha no login. Email ou senha incorretos.', 'alert_error')

    # Verifica se o botão de criar conta foi clicado e o formulário é válido
    elif 'botao_submit_criarconta' in request.form and form_criarconta.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript
        )
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert_success')
        return redirect(url_for('home'))

    # Renderiza a página com os dois formulários
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Saindo!', 'alert_success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static',filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def post_criar():
    form_post = FormCriarPost()
    if form_post.validate_on_submit():
        post = Post(
            titulo=form_post.titulo.data,
            corpo=form_post.corpo.data,
            autor=current_user, # usuário atual
        )
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html',form_post=form_post)

def salvar_imagem(imagem):
    # Adicionar o código no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename) # separa o nomme da imagem da extensao
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    # Reduzir e  imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida = ImageOps.exif_transpose(imagem_reduzida) # gira a imagem
    imagem_reduzida.thumbnail(tamanho)

    # Salvar imagem
    imagem_reduzida.save(caminho_completo)

    return nome_arquivo

# def atualizar_cursos(form_editar):
#     lista_cursos = []
#     for nome_campo, campo in form_editar._fields.items():#form_editar._fields.items() evita o uso do gerador interno que dispara StopIteration.
#         if 'curso_' in nome_campo and campo.data: #campo.data-garante que só cursos marcados (True) sejam adicionados.
#             lista_cursos.append(campo.label.text)
#     return ';'.join(lista_cursos) # transforma a lista de cursos em uma string separada por ;

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data: # se o campo estiver marcado
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos) # transforma a lista de cursos em uma string separada por ;

# Lembrando: Quando clica no formulário enviando um method POST do formulário para o site (request do method POST)
@app.route('/perfil/editar', methods=['GET', 'POST']) # toda página que tem formulário tem que dizer que o método POST é permitido
@login_required
def perfil_editar():
    form_editar = FormEditarPerfil()
    if form_editar.validate_on_submit():
        #atualiza o e-mail do usuário logado com o valor digitado no formulário. É usada para salvar a nova informação
        # antes de gravar no banco de dados com db.session.commit().'
        current_user.email = form_editar.email.data
        current_user.username = form_editar.username.data

        if form_editar.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editar.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        current_user.cursos = atualizar_cursos(form_editar)

        database.session.commit()
        flash('Perfil atualizado com Sucesso!', 'alert_success')
        return redirect(url_for('perfil'))

    elif request.method == 'GET': # Para que o fomulário já apareça com o campo preenchido
        form_editar.email.data = current_user.email
        form_editar.username.data = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editar=form_editar)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor: # se o usuário atual é o autor do post
        form_editarpost = FormCriarPost()
        if request.method == 'GET': # se estiver carregando a página
            form_editarpost.titulo.data = post.titulo
            form_editarpost.corpo.data = post.corpo
        elif form_editarpost.validate_on_submit():#Essa condição só será verdadeira se o usuário clicou no botão de
            # envio e os dados estão corretos.
            post.titulo = form_editarpost.titulo.data # pega o texto digitado no campo "título".
            post.corpo = form_editarpost.corpo.data
            database.session.commit() # como o post já existe pode dar o commit direto
            flash('Post Atualizado com Sucesso!', 'alert-success')
            return redirect(url_for('home'))

    else:
        form_editarpost = None

    return render_template('post.html', post=post, form_editarpost=form_editarpost)



@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403) # abort(403) - é um erro que entrou em um link que não tem autorização

