from flet import *
import flet as ft
import sqlite3

class Login:

    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Login"
        self.page.bgcolor = "#f0f0f0"
        self.page.padding = 50
        self.page.window_resizable = False

        # Campos de entrada
        self.email_field = TextField(label="Email", width=300, icon=icons.EMAIL, border_color=ft.colors.BLUE_GREY_300, focused_border_color=ft.colors.BLUE)
        self.senha_field = TextField(label="Senha", width=300, password=True, icon=icons.LOCK, border_color=ft.colors.BLUE_GREY_300, focused_border_color=ft.colors.BLUE)

        # Checkbox para mostrar/ocultar senha
        self.show_password = Checkbox(label="Ver senha", value=False, on_change=self.toggle_password)

        # Botão de login
        self.login_button = ElevatedButton(text="Entrar", on_click=self.login, width=300, height=50, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)

        layout = Container(
                content=Column(
                    controls=[
                        Row(
                            controls=[
                                Image(src="Atividade001/PDV/img/login.jpg", width=150, height=150)
                            ],
                            alignment="center"
                        ),
                        self.email_field,
                        self.senha_field,
                        Row(
                            controls=[self.show_password],
                            alignment="center"
                        ),
                        self.login_button,
                        Row(
                            controls=[
                                Text("Não tem uma conta?", color=ft.colors.BLACK),
                                ft.TextButton("Inscreva-se!", on_click=lambda e: self.page.go("/register"))
                            ],
                            alignment="center",
                            vertical_alignment="center"
                        )
                    ],
                    alignment="center",
                    horizontal_alignment="center", 
                    spacing=10,
                    height=500,
                ),
                alignment=alignment.center,
                padding=padding.all(50),
                border_radius=10,
                bgcolor=ft.colors.WHITE,
                shadow=BoxShadow(blur_radius=20, spread_radius=5, color=ft.colors.BLUE_GREY_300)
            )
        # Layout
        self.page.add(layout)

    # Alternar exibição da senha
    def toggle_password(self, e):
        self.senha_field.password = not self.show_password.value
        self.page.update()

    # Função de login
    def login(self, e):
        email = self.email_field.value
        senha = self.senha_field.value

        conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')  # Substitua pelo caminho do seu banco de dados
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cadastros_Usuarios WHERE email=? AND senha=?", (email, senha))
        user = cursor.fetchone()

        if user:
            self.show_alert("Login efetuado com sucesso!", "Bem-vindo!", "success")
        else:
            self.show_alert("Hmm, algo deu errado.", "Seu login NÃO foi encontrado. E-mail ou Senha incorretos! Não possui uma conta? Crie uma!", "error")

        conn.close()

    # Função para exibir alerta
    def show_alert(self, title, text, icon):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(text),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_alert())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.page.update()

    def close_alert(self):
        self.page.dialog.open = False
        self.page.update()

ft.app(target=Login)
