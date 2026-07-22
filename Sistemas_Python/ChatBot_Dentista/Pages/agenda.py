import sqlite3
from pathlib import Path
import flet as ft


def _get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "db" / "clinica.db"


def buscar_consultas():
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            p.nome,
            c.data_consulta,
            c.horario,
            c.status
        FROM consultas c
        JOIN pacientes p
            ON p.id = c.paciente_id
        ORDER BY c.data_consulta, c.horario
        """
    )

    dados = cursor.fetchall()
    conexao.close()
    return dados


def build_agenda_page(page: ft.Page):
    lista_consultas = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

    def carregar_consultas(e=None):
        lista_consultas.controls.clear()
        consultas = buscar_consultas()

        if not consultas:
            lista_consultas.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Nenhuma consulta cadastrada.",
                        size=18,
                        color=ft.Colors.GREY_700,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(12),
                    border=ft.Border.all(1, ft.Colors.BLUE_100),
                )
            )
        else:
            for nome, data, horario, status in consultas:
                cor_status = ft.Colors.BLUE_600
                status_texto = str(status or "").strip().lower()
                if status_texto == "confirmada":
                    cor_status = ft.Colors.GREEN_600
                elif status_texto == "pendente":
                    cor_status = ft.Colors.ORANGE_600

                lista_consultas.controls.append(
                    ft.Card(
                        elevation=2,
                        content=ft.Container(
                            padding=20,
                            content=ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(nome, size=18, weight=ft.FontWeight.BOLD),
                                            ft.Text(f"{data} • {horario}", color=ft.Colors.GREY_700),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            status,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                        bgcolor=cor_status,
                                        border_radius=ft.BorderRadius.all(20),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ),
                    )
                )

        page.update()

    btn_atualizar = ft.ElevatedButton(
        "Atualizar",
        icon=ft.Icons.REFRESH,
        on_click=carregar_consultas,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    btn_nova_consulta = ft.OutlinedButton(
        "Nova consulta",
        icon=ft.Icons.ADD,
        style=ft.ButtonStyle(
            color=ft.Colors.BLUE_700,
            side=ft.BorderSide(1, ft.Colors.BLUE_300),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    top_bar = ft.Container(
        padding=20,
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Agendamentos", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text("Gerencie os compromissos da clínica", color=ft.Colors.GREY_700),
                    ]
                ),
                ft.Row([btn_atualizar, btn_nova_consulta], spacing=10),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    content = ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                top_bar,
                ft.Text("Próximas consultas", size=20, weight=ft.FontWeight.BOLD),
                lista_consultas,
            ],
            spacing=20,
        ),
    )

    carregar_consultas()
    return content
