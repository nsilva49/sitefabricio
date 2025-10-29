# Para criar as tabelas do banco de dados

from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) # como o id_usuario é a chave primaria, pode usar o get direto para
    # encontrar o usuário pelo id


class Usuario(database.Model, UserMixin): # irá herdar todas as informações do database.Model (inclusive o init)
    id= database.Column ('id', database.Integer, primary_key=True) # o id será um valor único e servirá como chave primária.
    username= database.Column ('username', database.String, nullable=False) #nullable=False-deverá ter um nome preenchido
    email= database.Column ('email', database.String, nullable=False, unique=True) #unique=True-o email não pode repetir
    senha = database.Column ('senha', database.String,nullable=False)
    foto_perfil= database.Column ('foto_perfil', database.String, default='default.jpg')#default='default.jpg'- será um formato fixo de imagem, no caso jpg
    posts= database.relationship('Post', backref='autor', lazy=True)# nome do post(autor), passa todas a informações do autor(lazy=True)
    cursos= database.Column('cursos', database.String, nullable=False, default='Não Informado')# default='Não Informado'-será o valor padrão antes de ser digitado algo

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id= database.Column ('id', database.Integer, primary_key=True)
    titulo= database.Column ('titulo', database.String, nullable=False)
    corpo= database.Column ('corpo', database.Text, nullable=False)
    data_criacao= database.Column ('data_criacao',database.DateTime,nullable=False,default=datetime.utcnow)
    # default=datetime.utcnow- Ele faz com que, quando um novo registro for criado e nenhum valor for fornecido para essa
    # coluna, o valor padrão seja a data e hora atual em UTC.S
    id_usuario = database.Column('id_usuario', database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    #database.ForeignKey('usuario.id'). Esse campo é usado para relacionar registros de uma tabela com os da tabela
    # usuario. Por exemplo, se você tiver uma tabela de postagens, cada postagem pode estar associada a um usuário
    # por meio dessa chave estrangeira.