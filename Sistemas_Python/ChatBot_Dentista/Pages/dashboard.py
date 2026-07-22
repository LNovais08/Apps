import sqlite3
from pathlib import Path
import flet as ft


def _get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "db" / "clinica.db"


def _contar_registros(tabela: str, campo: str = "id") -> int:
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute(f"SELECT COUNT({campo}) FROM {tabela}")
    resultado = cursor.fetchone()[0]
    conexao.close()
    return resultado or 0


def _contar_status(status: str) -> int:
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM consultas WHERE status = ?", (status,))
    resultado = cursor.fetchone()[0]
    conexao.close()
    return resultado or 0


def build_dashboard_page(page: ft.Page):
    total_consultas = _contar_registros("consultas")
    total_pacientes = _contar_registros("pacientes")
    confirmadas = _contar_status("confirmada")
    pendentes = _contar_status("pendente")

    cards = [
        ft.Container(
            content=ft.Column([
                ft.Text("Consultas", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(str(total_consultas), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ], spacing=4),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=ft.BorderRadius.all(12),
            expand=True,
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Confirmadas", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(str(confirmadas), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
            ], spacing=4),
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=ft.BorderRadius.all(12),
            expand=True,
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Pendentes", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(str(pendentes), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
            ], spacing=4),
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=ft.BorderRadius.all(12),
            expand=True,
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Pacientes", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(str(total_pacientes), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
            ], spacing=4),
            padding=20,
            bgcolor=ft.Colors.PURPLE_50,
            border_radius=ft.BorderRadius.all(12),
            expand=True,
        ),
    ]

    return ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Resumo rápido da clínica", color=ft.Colors.GREY_700),
                ft.Row(cards, spacing=12, wrap=True),
                ft.Container(
                    content=ft.Text(
                        "Acompanhe o volume de consultas e a situação dos pacientes em um só lugar.",
                        size=16,
                        color=ft.Colors.GREY_700,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=ft.BorderRadius.all(12),
                ),
            ],
            spacing=20,
        ),
    )
