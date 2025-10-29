# Para rodar o programa

from comunidadeimpressionadora import app # como é do arquivo init não precisa escrever comunidadeimpressionadora.init

if __name__ == '__main__':  # Garante que o app só rode se este arquivo for o principal
    app.run(debug=True)  # Executa o servidor com modo debug ativado, evita que toda vez que atualizar
                         # o site tenha que pausar e rodar de novo

