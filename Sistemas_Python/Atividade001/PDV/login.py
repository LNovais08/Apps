from flet import *
import flet as ft
import sqlite3
import os
import subprocess
import json

def main(page: ft.Page):
    page.theme_mode = "light"
    page.title = "Página Login"
    page.window.center()
    page.padding = 0
    page.window_resizable = False
    page.appbar=ft.AppBar(
        leading=ft.Icon(ft.icons.SHOPPING_CART),
        title=ft.Text("SuperMarket"),
        actions=[
            ft.IconButton(icon=ft.icons.HEART_BROKEN)
        ],
        bgcolor=ft.colors.BLUE_GREY_100
    )

    email_login = ft.TextField(label="E-mail", width=450, color="black", text_size=15,border=ft.InputBorder.UNDERLINE,filled=True, prefix_icon=ft.icons.PERSON)
    senha_login = ft.TextField(label="Senha", width=450, color="black", password=True, can_reveal_password=True, text_size=15,border=ft.InputBorder.UNDERLINE,filled=True,  prefix_icon=ft.icons.KEY)

    # Botão de Login
    def logar_clicked(e):
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
                conn = sqlite3.connect('./db/cadastrosU.db')
                cursor = conn.cursor()
            
                cursor.execute("SELECT * FROM cadastros_Usuarios WHERE email=? AND senha=?", (email1, senha1))
                result = cursor.fetchone()
                conn.close()
                if result:
                    # Armazena as informações do usuário em um arquivo temporário
                    user_info = {
                        'id': result[0],
                        'nome': result[1],
                        'email': result[3],
                        'sexo': result[4],
                        'grau': result[5]
                    }
                    with open("./temp_user_info.json", "w") as temp_file:
                        json.dump(user_info, temp_file)
                    # Fecha a tela atual
                    page.window.close()
                    print('Abrindo pagina 2')
                    # Executa outro script Python
                    script_path = "./principal/pdv.py"
                    os.system(f"flet run {script_path}")
                        #subprocess.call(["python", script_path])
                else:
                    email_login.error_text = "E-mail ou senha incorretos"
                    senha_login.value = ""
                    page.update()

    logar = ft.ElevatedButton(text="Logar", width=150, height=50, color="white", bgcolor="black", on_click=logar_clicked)

    # Criando o contêiner de login
    login = ft.Container(
            content=ft.Column(
            controls=[ft.Text("Login", color="Black", size=35), email_login, senha_login, logar],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=26
        ),
        expand=True,
        alignment=ft.alignment.center,
    )
    
    main = ft.ResponsiveRow(
        [
            ft.Container(
                content=ft.Image(
                    src='./img/login2.jpg',
                    fit=ft.ImageFit.COVER, 
                ),
                alignment=ft.alignment.center,
                expand=True,
                col={"sm": 6, "md": 6, "xl": 6},
            ),
            ft.Container(
                content=login,
                alignment=ft.alignment.center,
                expand=True,
                col={"sm": 6, "md": 6, "xl": 6},
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.add(main)

ft.app(target=main)