from flet import *
import flet as ft
import sqlite3

def main(page: Page):
    # Definindo o título da página
    page.title = "Página Login"

    # Criando o contêiner principal
    principal = ft.Container(
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.center,
        expand=True
    )

    # Criando o contêiner tela com imagem de fundo
    img_container = ft.Container(
        content=ft.Image(
            src='Atividade001/Login/img/login.jpg',
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        expand=True,
    )

    # Função para conectar ao banco de dados e criar a tabela se não existir
    def init_db():
        conn = sqlite3.connect('Atividade001/Login/bd/logins.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logins
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, senha TEXT)''')
        conn.commit()
        conn.close()

    # Inicializa o banco de dados
    init_db()
    
    def show_logado_page():
        page.clean()
        # Itens para Login
        nonlocal email_login, senha_login
        text_login = ft.Text("Logado", color="Black", size=35)
        # Criando o contêiner de login
        login = ft.Container(
            content=ft.Column(
                controls=[text_login, logado],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor=ft.colors.WHITE,
            width=595,
            height=670,
            alignment=ft.alignment.center
        )
        principal.content = ft.Row(
            controls=[img_container, login],
            alignment=ft.MainAxisAlignment.CENTER,  # Centralizando os contêineres na tela
            expand=True
        )
        page.add(principal)
        page.update()

    def show_login_page():
        page.clean()
        # Itens para Login
        nonlocal email_login, senha_login
        text_login = ft.Text("Login", color="Black", size=35)
        email_login = ft.TextField(label="E-mail", width=450, color="black", text_size=15)
        senha_login = ft.TextField(label="Senha", width=450, color="black", password=True, can_reveal_password=True, text_size=15)
        logar = ft.ElevatedButton(text="Logar", width=150, height=35, color="white", on_click=entrar)
        link = ft.TextButton("Clique aqui para se Cadastrar", on_click=link_clicked)

        # Criando o contêiner de login
        login = ft.Container(
            content=ft.Column(
                controls=[text_login, email_login, senha_login, logar, link],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor=ft.colors.WHITE,
            width=595,
            height=670,
            alignment=ft.alignment.center
        )
        principal.content = ft.Row(
            controls=[img_container, login],
            alignment=ft.MainAxisAlignment.CENTER,  # Centralizando os contêineres na tela
            expand=True
        )
        page.add(principal)
        page.update()

    def link_clicked(e):
        def cadastrar(e):
            nome1 = nome.value
            email1 = email.value
            senha1 = senha.value
            if not email1:
                email.error_text = "Preencha seu E-mail"
                page.update()
            elif not senha1:
                senha.error_text = "Preencha sua Senha"
                page.update()
            elif not nome1:
                nome.error_text = "Preencha seu Nome"
                page.update()
            else:
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('Atividade001/Login/bd/logins.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO logins (nome, email, senha) VALUES (?, ?, ?)", (nome1, email1, senha1))
                conn.commit()
                conn.close()
                show_login_page()

        # Itens para Cadastro
        nonlocal nome, email, senha
        text_cadastro = ft.Text("Cadastro", color="Black", size=35)
        nome = ft.TextField(label="Nome", width=450, color="black", text_size=15)
        email = ft.TextField(label="E-mail", width=450, color="black", text_size=15)
        senha = ft.TextField(label="Senha", width=450, color="black", password=True, can_reveal_password=True, text_size=15)
        cadastrar_btn = ft.ElevatedButton(text="Cadastrar", width=150, height=35, color="white", on_click=cadastrar)

        cadastro = ft.Container(
            content=ft.Column(
                controls=[text_cadastro, nome, email, senha, cadastrar_btn],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor=ft.colors.WHITE,
            width=595,
            height=670,
            alignment=ft.alignment.center
        )
                
        principal.content = ft.Row(
            controls=[img_container, cadastro],
            alignment=ft.MainAxisAlignment.CENTER,  # Centralizando os contêineres na tela
            expand=True
        )
        page.add(principal)
        page.update()
        
    def entrar(e):
        email1 = email_login.value
        senha1 = senha_login.value
        if not email1:
            email_login.error_text = "Preencha seu E-mail"
            page.update()
        elif not senha1:
            senha_login.error_text = "Preencha sua Senha"
            page.update()
        else:
            # Conecta ao banco de dados e insere os valores
            conn = sqlite3.connect('Atividade001/Login/bd/logins.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logins WHERE email=? AND senha=?", (email1, senha1))
            result = cursor.fetchone()
            conn.close()
            if result:
                page.clean()
                nonlocal logado
                logado = ft.Text(f"Bem-vindo, {result[0]}  ||  {result[1]}!", size=25, color="black")
                show_logado_page()
            else:
                email_login.error_text = "E-mail ou senha incorretos"
                senha_login.value = ""
                page.update()

    # Inicializa as variáveis de controle como None
    email_login = None
    senha_login = None
    nome = None
    email = None
    senha = None
    logado = None
    show_login_page()

ft.app(target=main)
