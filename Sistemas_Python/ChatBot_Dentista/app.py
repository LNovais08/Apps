import flet as ft
from Pages.agenda import build_agenda_page
from Pages.dashboard import build_dashboard_page
from Pages.pacientes import build_pacientes_page


def main(page: ft.Page):
    page.title = "Clínica Odontológica"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.window.resizable = False
    page.window.maximized = True

    def navegar_pagina(destino: str):
        if destino == "agenda":
            conteudo_principal.content = build_agenda_page(page)
        elif destino == "pacientes":
            conteudo_principal.content = build_pacientes_page(page)
        else:
            conteudo_principal.content = build_dashboard_page(page)
        page.update()

    sidebar = ft.Container(
        width=page.width * 0.40,
        bgcolor=ft.Colors.BLUE_900,
        padding=10,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            controls=[
                ft.Image(
                    src="Sistemas_Python/ChatBot_Dentista/img/logo.png",
                    width=220,
                    height=220,
                ),
                ft.Text(
                    "Clínica Odontológica",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Painel administrativo",
                    size=20,
                    color=ft.Colors.BLUE_100,
                ),
                ft.Divider(color=ft.Colors.BLUE_700),
                ft.Container(height=10),
                ft.TextButton(
                    content=ft.Text("Dashboard", size=18),
                    icon=ft.Icons.DASHBOARD,
                    on_click=lambda e: navegar_pagina("dashboard"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                ),
                ft.TextButton(
                    content=ft.Text("Agendamentos", size=18),
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda e: navegar_pagina("agenda"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                ),
                ft.TextButton(
                    content=ft.Text("Pacientes", size=18),
                    icon=ft.Icons.PERSON,
                    on_click=lambda e: navegar_pagina("pacientes"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                ),
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    conteudo_principal = ft.Container(
        expand=True,
        padding=20,
        bgcolor=ft.Colors.WHITE,
    )

    page.add(
        ft.Row(
            controls=[sidebar, conteudo_principal],
            spacing=0,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )

    navegar_pagina("dashboard")


ft.app(target=main)
