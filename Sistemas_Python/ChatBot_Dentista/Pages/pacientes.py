import sqlite3
from pathlib import Path
import flet as ft


def _get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "db" / "clinica.db"


def buscar_pacientes():
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT nome, telefone, email FROM pacientes ORDER BY nome")
    except sqlite3.Error:
        cursor.execute("SELECT nome FROM pacientes ORDER BY nome")
        dados = [(nome,) for (nome,) in cursor.fetchall()]
        conexao.close()
        return dados

    dados = cursor.fetchall()
    conexao.close()
    return dados


def build_pacientes_page(page: ft.Page):
    lista_pacientes = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
    pacientes = buscar_pacientes()

    if not pacientes:
        lista_pacientes.controls.append(
            ft.Container(
                content=ft.Text("Nenhum paciente cadastrado.", size=18, color=ft.Colors.GREY_700),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=ft.BorderRadius.all(12),
                border=ft.Border.all(1, ft.Colors.BLUE_100),
            )
        )
    else:
        for paciente in pacientes:
            nome = paciente[0]
            detalhes = ""
            if len(paciente) > 1 and paciente[1]:
                detalhes = str(paciente[1])
            if len(paciente) > 2 and paciente[2]:
                detalhes = f"{detalhes} • {paciente[2]}".strip(" •")

            lista_pacientes.controls.append(
                ft.Card(
                    elevation=2,
                    content=ft.Container(
                        padding=20,
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(nome, size=18, weight=ft.FontWeight.BOLD),
                                        ft.Text(detalhes or "Sem informações adicionais", color=ft.Colors.GREY_700),
                                    ],
                                    expand=True,
                                ),
                                ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_600),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ),
                )
            )

    return ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text("Pacientes", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Lista dos pacientes cadastrados", color=ft.Colors.GREY_700),
                lista_pacientes,
            ],
            spacing=20,
        ),
    )
