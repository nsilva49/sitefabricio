from comunidadeimpressionadora import app,database, bcrypt
#from models import Usuario, Post
from comunidadeimpressionadora.models import Usuario, Post


# Todo comando que será executado dentro do banco de dados deverá estar dentro do
# with app.app.contextt()

# #Criando o banco de dados
# with app.app_context():
#     database.create_all()
#
# #with app.app_context():
#     usuario = Usuario(username='Fabrício', email='fabrinogueira@yahoo.com.br', senha='123456')
#     usuario2 = Usuario(username='Luísa', email='luisanogueira@yahoo.com.br', senha='123456')
#
#     # Adicionando os usuários na sessão do banco de dados
#     database.session.add(usuario)
#     database.session.add(usuario2)
#
#     # Salvando as alterações no banco de dados
#     database.session.commit()

# with app.app_context():
#     # Pegar todas as informações do banco de dados
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#     primeiro_usuario = Usuario.query.first()
#     print(primeiro_usuario.id)
#     print(primeiro_usuario.email)
#     print(primeiro_usuario.posts)
#
#     # Usando o filtro para pegar informações do bd
#     # Está pegando o nome do usuário cujo o email é 'fabrinogueira@yahoo.com.br'
#     usuario_teste = Usuario.query.filter_by(email='fabrinogueira@yahoo.com.br').first()
#     print(usuario_teste)
#     print(usuario_teste.username)
#
# with app.app_context():
#     meu_post = Post(id_usuario=1, titulo='Primeiro Post do Fabrício', corpo='Deus abençoe meus estudos')
#     database.session.add(meu_post)
#     database.session.commit()


# with app.app_context():
#     post = Post.query.first()
#     print(post.titulo)
#     print(post.autor.email) # autor - foi o nome do post que foi dado dentro da calsse "Usuario"
#     print(post.autor.username)

# with app.app_context():
#     database.drop_all() # deleta o bd
# #     database.create_all() # cria o bd
# with app.app_context():
#     Usuario.query.all()
#     meus_usuarios = Usuario.query.first()
#     print(meus_usuarios.username)
#     print(meus_usuarios.email)
#     print(meus_usuarios.senha)
#
#     print('-'* 80)
#
#     usuario2= Usuario.query.filter_by(username='Luisa').first()
#     print(usuario2.username)
#     print(usuario2.email)
#     print(usuario2.senha)
#
# senha='123456'
# senha_bcrypt = bcrypt.generate_password_hash(senha).decode('utf-8') # criptografa a senha. Se você for salvar
# # senha_bcrypt no banco, é melhor decodificar para string
# print(bcrypt.check_password_hash(senha_bcrypt, senha)) # verifica se a senha digitada é igual a senha criptografada

# ⚠ Cuidado com isso em produção!

# with app.app_context():
#     database.drop_all()  # Apaga todas as tabelas
#     database.create_all()  # Cria todas as tabelas novamente
#     print("Banco de dados apagado e recriado com sucesso.")


with app.app_context():
#     usuario = Usuario.query.filter_by(email='fabrinogueira@yahoo.com.br').first()
#     print(usuario.cursos)

    post = Post.query.first()
    print(post.titulo)



    # with app.app_context():
#     meus_usuarios = Usuario.query.first()
#     print(meus_usuarios.username)
#     print(meus_usuarios.email)
#     print(meus_usuarios.senha)
#     print('-' * 80)
#
#     usuario2 = Usuario.query.filter_by(username='Luisa').first()
#     if usuario2:
#         print(usuario2.username)
#         print(usuario2.email)
#         print(usuario2.senha)
#
# senha = '123456'
# senha_bcrypt = bcrypt.generate_password_hash(senha).decode('utf-8')
# print(bcrypt.check_password_hash(senha_bcrypt, senha))  # Deve imprimir True
