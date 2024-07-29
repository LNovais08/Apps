from flet import *
import flet as ft
import sqlite3
import subprocess

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
            nome1 = Nome.value
            tel1 = Tel.value
            email1 = Email.value
            sexo1 = sexo.value
            senha1 = senha.value
            adm1 = adm.value
            if not email1:
                Email.error_text = "Preencha seu E-mail"
                page.update()
            elif not senha1:
                senha.error_text = "Preencha sua Senha"
                page.update()
            elif not nome1:
                Nome.error_text = "Preencha seu Nome"
                page.update()
            elif not sexo1:
                sexo.error_text = "Preencha qual o seu Sexo"
                page.update()
            elif not tel1:
                Tel.error_text = "Preencha seu Telefone"
                page.update()
            else:
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cadastros_Usuarios (nome, Tel, email, sexo, grau, senha) VALUES (?, ?, ?, ?, ?, ?)", (nome1, tel1, email1, sexo1, adm1, senha1))
                conn.commit()
                conn.close()
                Nome.value = ""
                Tel.value = ""
                Email.value = ""
                sexo.value = ""
                adm.value = ""
                senha.value = ""
                page.update()
                       
        # Função para formatar e validar o telefone
        def format_telefone(e):
            raw_tel = ''.join(filter(str.isdigit, Tel.value))[:11]  # Somente dígitos e max 11 caracteres
            formatted_tel = raw_tel
            if len(raw_tel) > 10:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:7]}-{raw_tel[7:11]}"
            elif len(raw_tel) > 6:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:6]}-{raw_tel[6:]}"
            elif len(raw_tel) > 2:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:]}"
            Tel.value = formatted_tel
            page.update()

        def dropdown_changed(e):
            adm.value = adm.value
            page.update()
        
        # Itens para Cadastro de Usuário
        Nome = ft.TextField(label="Nome", width=450, color="black", text_size=15, border_color="gray")
        Tel = ft.TextField(label="Telefone", width=450, color="black", text_size=15, border_color="gray", on_change=format_telefone)
        Email = ft.TextField(label="E-mail", width=450, color="black", border_color="gray")
        sexo = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="Feminino", label="Feminino"),
                ft.Radio(value="Masculino", label="Masculino")
            ], alignment=ft.MainAxisAlignment.CENTER),
        ) 
        adm = ft.Dropdown(
            width=450,
            on_change=dropdown_changed,
            options=[
                ft.dropdown.Option("Admin"),
                ft.dropdown.Option("Funcionário"),
            ],
        ) 
        senha = ft.TextField(label="Senha", width=450, color="black", password=True, can_reveal_password=True, text_size=15, border_color="gray")
        cadastrar_btn = ft.ElevatedButton(text="Cadastrar", width=150, height=35, color="white", on_click=cadastrar)

        cadastro = ft.Container(
            content=ft.Column(
                controls=[Nome, Tel, Email, sexo, adm, senha, cadastrar_btn],
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
            conn = sqlite3.connect('PDV/db/cadastrosU.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cadastros_Usuarios WHERE email=? AND senha=?", (email1, senha1))
            result = cursor.fetchone()
            conn.close()
            if result:
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
