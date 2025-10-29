from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)  # Inicializa a aplicação Flask

# Configurações da aplicação
#Path(__file__): cria um objeto de caminho para o arquivo atual (por exemplo, __init__.py)
#.parent: acessa a pasta onde esse arquivo está
#/"comunidade.db": junta o nome do arquivo do banco de dados ao caminho da pasta
dp_path =Path(__file__).parent/"comunidade.db"

#URL_PÚBLICA_MYSQL
#"URL_MYSQL"
if os.getenv("DATABASE_PUBLIC_URL"):
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_PUBLIC_URL")

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dp_path}'  # Caminho do banco de dados


# Chave secreta
app.config['SECRET_KEY'] = '20c4aa37d6cc6be00f8e19695023561d'



# Inicializa o banco de dados com as configurações já definidas
database = SQLAlchemy(app)

bcrypt = Bcrypt(app) # criptografar senha

login_manager = LoginManager(app) #Associa essa instância ao seu aplicativo Flask (app), permitindo que o
# Flask-Login controle o login dos usuários.

login_manager.login_view = 'login' # A linha login_manager.login_view = 'login' define que, se um usuário
# não autenticado tentar acessar uma rota protegida por @login_required, ele será redirecionado para
# a rota chamada 'login'.

login_manager.login_message_category = 'alert-info' # Configura a mensagem de alerta caso não esteja logado

# Importa as rotas (deve ser feito após a criação do app e do banco)
from comunidadeimpressionadora import routes



