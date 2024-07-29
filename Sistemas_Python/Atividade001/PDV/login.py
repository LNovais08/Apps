from flet import *
import flet as ft
import sqlite3
import subprocess
import sys

def main(page: Page):
    # Definindo o título da página
    page.title = "Página Login"
    # Centralizar a janela na tela
    page.window_center()

    # Criando o contêiner principal
    principal = ft.Container(
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.center,
        expand=True
    )

    # Criando o contêiner tela com imagem de fundo
    img_container = ft.Container(
        content=ft.Image(
            src='PDV/img/login2.jpg',
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        expand=True,
    )

    # Função para conectar ao banco de dados e criar a tabela se não existir
    def init_db():
        conn = sqlite3.connect('PDV/db/cadastrosU.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cadastros_Usuarios
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, Tel TEXT ,email TEXT, sexo TEXT , grau TEXT,senha TEXT)''')
        conn.commit()
        conn.close()

    # Inicializa o banco de dados
    init_db()
    
    def show_login_page():
        page.clean()
        # Itens para Login
        nonlocal email_login, senha_login
        text_login = ft.Text("Login", color="Black", size=35)
        email_login = ft.TextField(label="E-mail", width=450, color="black", text_size=15)
        senha_login = ft.TextField(label="Senha", width=450, color="black", password=True, can_reveal_password=True, text_size=15)
        logar = ft.ElevatedButton(text="Logar", width=150, height=35, color="white", on_click=entrar)

        # Criando o contêiner de login
        login = ft.Container(
            content=ft.Column(
                controls=[text_login, email_login, senha_login, logar],
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
            conn = sqlite3.connect('PDV/db/cadastrosU.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cadastros_Usuarios WHERE email=? AND senha=?", (email1, senha1))
            result = cursor.fetchone()
            conn.close()
            if result:
                # Fecha a tela atual
                page.window_close()
                # Executa outro script Python
                script_path = "c:\\Users\\Lais\\OneDrive\\Documentos\\GitHub\\CursoSENAC\\Apps\\Sistemas_Python\\Atividade001\\PDV\\pdv.py"
                subprocess.call(["python", script_path])
            else:
                email_login.error_text = "E-mail ou senha incorretos"
                senha_login.value = ""
                page.update()

    # Inicializa as variáveis de controle como None
    email_login = None
    senha_login = None

    show_login_page()

ft.app(target=main)
