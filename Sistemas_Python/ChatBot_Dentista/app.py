import flet as ft
import sqlite3


def buscar_consultas():

    conexao = sqlite3.connect("ChatBot_Dentista/db/clinica.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            p.nome,
            c.data_consulta,
            c.horario,
            c.status
        FROM consultas c
        JOIN pacientes p
            ON p.id = c.paciente_id
        ORDER BY c.data_consulta, c.horario
    """)

    dados = cursor.fetchall()

    conexao.close()

    return dados


def main(page: ft.Page):

    page.title = "Clínica Odontológica"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.center()
    page.padding = 0
    page.window.resizable = False
    page.window.width = 1000
    page.window.height = 700
    

    tabela = ft.Column(scroll=ft.ScrollMode.AUTO)

    def carregar_consultas(e=None):

        tabela.controls.clear()

        consultas = buscar_consultas()

        if not consultas:

            tabela.controls.append(
                ft.Text(
                    "Nenhuma consulta cadastrada.",
                    size=18
                )
            )

        else:

            for nome, data, horario, status in consultas:

                tabela.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        nome,
                                        width=250,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        data,
                                        width=120
                                    ),
                                    ft.Text(
                                        horario,
                                        width=100
                                    ),
                                    ft.Text(
                                        status,
                                        width=120
                                    ),
                                ]
                            )
                        )
                    )
                )

        page.update()


    btn_atualizar = ft.TextButton(
        text="Atualizar",
        icon="REFRESH",
        width=250,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.TRANSPARENT,
            overlay_color=ft.colors.BLUE_300,
        ),
        on_click=carregar_consultas
    )
    navebar = ft.Container(
        padding=20,
        width = 250,
        height = 700,
        bgcolor=ft.colors.BLUE_100,
        content=ft.Column(
            controls=[
                ft.Image(
                    src="ChatBot_Dentista/img/logo.png",
                    width= 370,
                    height= 150,
                ),
                ft.Text(
                    "Clínica Odontológica",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                btn_atualizar,
                ft.Divider(),
                tabela
            ]
        )
    )
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    navebar,
                ]
            )
        )
    )

    carregar_consultas()


ft.app(target=main)