# Arquivo de Fomulários
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # FileField(campo de arquivo),FileAllowed(validador,é onde escolhe as extensões dos arquivos)
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError #DataRequired-obrigatório
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(),
        Email()
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, max=20)
    ])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')



class FormCriarConta(FlaskForm): # não insere o init na classe, pois, está usando o init do FlaskForm
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(min=6, max=20)]) # tamanho da senha entre 6 e 20 caracteres
    confirmacao = PasswordField('Confirmação da Senha',validators=[DataRequired(),EqualTo('senha')]) # EqualTo - que seja igual a senha
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email): # a função tem quer ter esse nome, pois, o validate_on_submit validar o email
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email cadastrado. Cadastre-se com outro email ou faça login para continuar.')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    email = StringField('Atualizar ', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil.', validators=[FileAllowed(['jpg', 'png'])])

    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sqla = BooleanField('SQL Impressionador')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    # Essa validação é para não deixar o usurário cadastrar um e-mail já existente
    def validate_email(self, email): # a função tem quer ter esse nome, pois, o validate_on_submit validar o email
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu Post Aqui.', validators=[DataRequired()])
    botao_submit_criarpost = SubmitField('Criar Post')

# class FormLogin(FlaskForm):
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     senha = PasswordField('Senha',validators=[DataRequired(),Length(min=6, max=20)])
#     lembrar_dados = BooleanField('Lembrar Dados de Acesso')
#     botao_submit_login = SubmitField('Fazer Login')
