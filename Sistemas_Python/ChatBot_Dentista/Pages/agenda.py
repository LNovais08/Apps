import calendar
import datetime
from pathlib import Path
import flet as ft

from database import buscar_consultas_do_mes, buscar_pacientes_agenda, inserir_consulta


def _gerar_dias_do_mes(ano: int, mes: int):
    calendario = calendar.Calendar(firstweekday=6)
    semanas = calendario.monthdayscalendar(ano, mes)
    dias = []
    for semana in semanas:
        for dia in semana:
            if dia == 0:
                dias.append({"day": 0, "is_current_month": False, "is_today": False, "appointments": []})
            else:
                hoje = datetime.date.today()
                data = datetime.date(ano, mes, dia)
                dias.append({
                    "day": dia,
                    "date": data,
                    "is_current_month": True,
                    "is_today": data == hoje,
                    "appointments": [],
                })
    return dias


def build_agenda_page(page: ft.Page):
    hoje = datetime.date.today()
    ano_atual = hoje.year
    mes_atual = hoje.month

    lista_consultas = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
    calendario_dias = []
    consultas_mes = []
    calendar_view = ft.Container(expand=1, content=ft.Text("Carregando calendário...", color=ft.Colors.GREY_700))

    modal_layer = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.BLACK_26,
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=560,
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=24,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_300, offset=ft.Offset(0, 3), spread_radius=0),
            content=ft.Column(controls=[], spacing=16),
        ),
    )

    paciente_dropdown = ft.Dropdown(
        label="Paciente",
        hint_text="Selecione um paciente cadastrado",
        width=250,
        options=[],
        autofocus=True,
    )
    horario_field = ft.TextField(label="Horário", hint_text="Ex.: 14:30", width=180)
    status_dropdown = ft.Dropdown(
        label="Status",
        width=180,
        options=[
            ft.dropdown.Option("PENDENTE"),
            ft.dropdown.Option("CONFIRMADA"),
            ft.dropdown.Option("CANCELADA"),
        ],
    )
    status_dropdown.value = "PENDENTE"
    selected_date_text = ft.Text("", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD)
    form_status = ft.Text("", visible=False, color=ft.Colors.GREEN_700)

    def fechar_modal(e=None):
        modal_layer.visible = False
        page.update()

    def abrir_modal(data_selecionada):
        nonlocal selected_date_text
        selected_date_text.value = f"Nova consulta para {data_selecionada.strftime('%d/%m/%Y')}"
        form_status.value = ""
        form_status.visible = False
        horario_field.value = ""
        status_dropdown.value = "PENDENTE"
        paciente_dropdown.value = None
        paciente_dropdown.options.clear()
        for paciente_id, nome in buscar_pacientes_agenda():
            paciente_dropdown.options.append(ft.dropdown.Option(key=str(paciente_id), text=nome))
        modal_layer.visible = True
        page.update()

    def salvar_consulta(e=None):
        if not paciente_dropdown.value:
            form_status.value = "Selecione um paciente cadastrado."
            form_status.color = ft.Colors.RED_600
            form_status.visible = True
            page.update()
            return
        if not horario_field.value.strip():
            form_status.value = "Informe o horário da consulta."
            form_status.color = ft.Colors.RED_600
            form_status.visible = True
            page.update()
            return

        data_texto = selected_date_text.value.split("para ")[-1]
        data_obj = datetime.datetime.strptime(data_texto, "%d/%m/%Y").date()
        inserir_consulta(
            paciente_id=int(paciente_dropdown.value),
            data_consulta=data_obj.strftime("%Y-%m-%d"),
            horario=horario_field.value.strip(),
            status=status_dropdown.value or "PENDENTE",
        )
        form_status.value = "Consulta agendada com sucesso!"
        form_status.color = ft.Colors.GREEN_700
        form_status.visible = True
        carregar_consultas()
        page.update()

    def carregar_consultas(e=None):
        nonlocal consultas_mes, calendario_dias
        lista_consultas.controls.clear()
        consultas = buscar_consultas_do_mes(ano_atual, mes_atual)
        consultas_mes = consultas
        calendario_dias = _gerar_dias_do_mes(ano_atual, mes_atual)

        for item in calendario_dias:
            if item.get("day") == 0:
                continue
            data = item["date"]
            qtd = sum(1 for c in consultas_mes if c[0] == data.strftime("%Y-%m-%d"))
            item["appointments"] = [c for c in consultas_mes if c[0] == data.strftime("%Y-%m-%d")]
            item["appointment_count"] = qtd

        if not consultas:
            lista_consultas.controls.append(
                ft.Container(
                    content=ft.Text("Nenhuma consulta cadastrada para este mês.", size=16, color=ft.Colors.GREY_700),
                    padding=18,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=12,
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                )
            )
        else:
            for data_consulta, horario, status, nome in consultas:
                cor_status = ft.Colors.BLUE_600
                status_texto = str(status or "").strip().lower()
                if status_texto == "confirmada":
                    cor_status = ft.Colors.GREEN_600
                elif status_texto == "pendente":
                    cor_status = ft.Colors.ORANGE_600
                elif status_texto == "cancelada":
                    cor_status = ft.Colors.RED_600

                lista_consultas.controls.append(
                    ft.Container(
                        padding=16,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=14,
                        border=ft.Border.all(1, ft.Colors.GREY_200),
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(nome, size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"{data_consulta} • {horario}", size=13, color=ft.Colors.GREY_700),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Text(status.upper(), color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=12),
                                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                                    bgcolor=cor_status,
                                    border_radius=20,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    )
                )

        calendar_view.content = renderizar_calendario()
        page.update()

    def renderizar_calendario():
        dias_da_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        cabecalho = ft.Row(
            controls=[
                ft.Text(f"{calendar.month_name[mes_atual]} {ano_atual}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        dias_header = ft.Row([
            ft.Container(width=42, content=ft.Text(d, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), alignment=ft.Alignment.CENTER)
            for d in dias_da_semana
        ], spacing=6)

        rows = []
        for inicio in range(0, len(calendario_dias), 7):
            semana = calendario_dias[inicio:inicio + 7]
            cells = []
            for item in semana:
                if item.get("day") == 0:
                    cells.append(ft.Container(width=42, height=64, bgcolor=ft.Colors.GREY_50, border_radius=12))
                    continue
                data = item["date"]
                qtd = item.get("appointment_count", 0)
                container = ft.Container(
                    width=42,
                    height=64,
                    bgcolor=ft.Colors.WHITE if item["is_current_month"] else ft.Colors.GREY_50,
                    border_radius=12,
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                    content=ft.Column(
                        controls=[
                            ft.Text(str(data.day), size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Text(f"{qtd} ag", size=10, color=ft.Colors.BLUE_700) if qtd else ft.Container(height=0),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    on_click=lambda e, d=data: abrir_modal(d),
                    ink=True,
                )
                if item["is_today"]:
                    container.bgcolor = ft.Colors.BLUE_50
                    container.border = ft.Border.all(1, ft.Colors.BLUE_300)
                cells.append(container)
            rows.append(ft.Row(controls=cells, spacing=6))

        return ft.Column(controls=[cabecalho, dias_header, *rows], spacing=12)

    def mudar_mes(delta):
        nonlocal ano_atual, mes_atual
        novo_mes = mes_atual + delta
        novo_ano = ano_atual
        while novo_mes < 1:
            novo_mes += 12
            novo_ano -= 1
        while novo_mes > 12:
            novo_mes -= 12
            novo_ano += 1
        ano_atual, mes_atual = novo_ano, novo_mes
        carregar_consultas()

    btn_atualizar = ft.ElevatedButton(
        "Atualizar",
        icon=ft.Icons.REFRESH,
        on_click=carregar_consultas,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10)),
    )
    btn_mes_anterior = ft.IconButton(ft.Icons.CHEVRON_LEFT, on_click=lambda e: mudar_mes(-1))
    btn_mes_seguinte = ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=lambda e: mudar_mes(1))

    modal_content = ft.Column(
        controls=[
            ft.Row([ft.Text("Agendar consulta", size=20, weight=ft.FontWeight.BOLD), ft.IconButton(ft.Icons.CLOSE, on_click=fechar_modal)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            selected_date_text,
            ft.Row([paciente_dropdown, horario_field], spacing=12),
            ft.Row([status_dropdown], spacing=12),
            form_status,
            ft.Row([ft.ElevatedButton("Salvar consulta", icon=ft.Icons.SAVE, on_click=salvar_consulta), ft.OutlinedButton("Cancelar", on_click=fechar_modal)], spacing=10),
        ],
        spacing=12,
    )
    modal_layer.content.content = modal_content

    top_bar = ft.Container(
        padding=20,
        content=ft.Row(
            controls=[
                ft.Column(controls=[ft.Text("Agendamentos", size=28, weight=ft.FontWeight.BOLD), ft.Text("Selecione um dia para agendar uma consulta", color=ft.Colors.GREY_700)], spacing=2),
                ft.Row([btn_mes_anterior, btn_mes_seguinte, btn_atualizar], spacing=6),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    content = ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            controls=[
                top_bar,
                ft.Container(
                    padding=24,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=20,
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                    shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_200, offset=ft.Offset(0, 3), spread_radius=0),
                    content=ft.Row(
                        controls=[
                            calendar_view,
                            ft.Container(
                                width=320,
                                padding=16,
                                bgcolor=ft.Colors.GREY_50,
                                border_radius=16,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Consultas do mês", size=18, weight=ft.FontWeight.BOLD),
                                        lista_consultas,
                                    ],
                                    spacing=12,
                                ),
                            ),
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ),
            ],
            spacing=20,
        ),
    )

    carregar_consultas()
    return ft.Stack(expand=True, controls=[content, modal_layer])
