import sqlite3
import re
from pathlib import Path
import flet as ft
from database import ensure_schema


def _get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "db" / "clinica.db"


def buscar_pacientes():
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, nome, cpf, data_nascimento, telefone, email, endereco, cidade, observacoes_medicas, ultima_consulta
        FROM pacientes
        ORDER BY nome
        """
    )
    dados = cursor.fetchall()
    conexao.close()
    return dados


def inserir_paciente(dados):
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO pacientes (
            nome, cpf, data_nascimento, telefone, email, endereco, cidade, observacoes_medicas, ultima_consulta
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        dados,
    )
    conexao.commit()
    conexao.close()


def atualizar_paciente(paciente_id, dados):
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE pacientes
        SET nome = ?, cpf = ?, data_nascimento = ?, telefone = ?, email = ?, endereco = ?, cidade = ?, observacoes_medicas = ?, ultima_consulta = ?
        WHERE id = ?
        """,
        (*dados, paciente_id),
    )
    conexao.commit()
    conexao.close()


def excluir_paciente(paciente_id):
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conexao.commit()
    conexao.close()


def _campo_formulario(label: str, icon: str, multiline: bool = False, height: int = 55, max_length: int = None):
    return ft.TextField(
        label=label,
        hint_text=label,
        icon=icon,
        multiline=multiline,
        min_lines=4 if multiline else 1,
        max_lines=6 if multiline else 1,
        height=height if multiline else 55,
        border_radius=12,
        border_color=ft.Colors.BLUE_100,
        focused_border_color=ft.Colors.BLUE_600,
        filled=True,
        bgcolor=ft.Colors.GREY_50,
        expand=1,
        dense=True,
        content_padding=ft.Padding.only(left=12, right=12, top=14, bottom=14),
        max_length=max_length,
    )


def _formatar_cpf(valor: str) -> str:
    numeros = re.sub(r"\D", "", valor or "")[:11]
    if len(numeros) <= 3:
        return numeros
    if len(numeros) <= 6:
        return f"{numeros[:3]}.{numeros[3:]}"
    if len(numeros) <= 9:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"


def _formatar_data(valor: str) -> str:
    numeros = re.sub(r"\D", "", valor or "")[:8]
    if len(numeros) <= 2:
        return numeros
    if len(numeros) <= 4:
        return f"{numeros[:2]}/{numeros[2:]}"
    return f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:]}"


def _formatar_telefone(valor: str) -> str:
    numeros = re.sub(r"\D", "", valor or "")[:11]
    if len(numeros) <= 2:
        return f"({numeros}"
    if len(numeros) <= 6:
        return f"({numeros[:2]}) {numeros[2:]}"
    if len(numeros) <= 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}"


def _formatar_texto_data(valor: str) -> str:
    if not valor or not str(valor).strip():
        return "Não tem última consulta"
    return _formatar_data(str(valor).strip())


def build_pacientes_page(page: ft.Page):
    # Campos do formulário
    nome_field = _campo_formulario("Nome completo", ft.Icons.PERSON_OUTLINE)
    cpf_field = _campo_formulario("CPF", ft.Icons.BADGE_OUTLINED, max_length=14)
    nascimento_field = _campo_formulario("Data de nascimento", ft.Icons.CALENDAR_TODAY, max_length=10)
    telefone_field = _campo_formulario("Telefone", ft.Icons.PHONE_ANDROID, max_length=15)
    email_field = _campo_formulario("E-mail", ft.Icons.EMAIL_OUTLINED)
    endereco_field = _campo_formulario("Endereço", ft.Icons.HOME_OUTLINED)
    cidade_field = _campo_formulario("Cidade", ft.Icons.LOCATION_ON_OUTLINED)
    ultima_consulta_field = _campo_formulario("Última consulta", ft.Icons.CALENDAR_MONTH)
    observacoes_field = _campo_formulario(
        "Observações médicas",
        ft.Icons.MEDICAL_INFORMATION_OUTLINED,
        multiline=True,
        height=120,
    )

    campos = [
        ("Nome completo", nome_field),
        ("CPF", cpf_field),
        ("Data de nascimento", nascimento_field),
        ("Telefone", telefone_field),
        ("E-mail", email_field),
        ("Endereço", endereco_field),
        ("Cidade", cidade_field),
        ("Última consulta", ultima_consulta_field),
        ("Observações médicas", observacoes_field),
    ]

    status_text = ft.Text("", visible=False, color=ft.Colors.GREEN_700)
    lista_pacientes = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
    paciente_editando_id = None

    modal_title = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    modal_info = ft.Column(controls=[], spacing=8, scroll=ft.ScrollMode.AUTO)
    modal_observacoes = ft.Column(controls=[], spacing=4)
    modal_layer = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.BLACK_54,
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=520,
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_300, offset=ft.Offset(0, 6), spread_radius=1),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=44,
                                height=44,
                                border_radius=22,
                                bgcolor=ft.Colors.BLUE_50,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_700, size=24),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Ficha do paciente", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                    ft.Text("Dados cadastrais completos", size=12, color=ft.Colors.GREY_600),
                                ],
                                spacing=1,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=ft.Colors.GREY_200),
                    modal_title,
                    modal_info,
                    ft.Container(
                        padding=12,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=12,
                        content=modal_observacoes,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Fechar",
                                icon=ft.Icons.CLOSE,
                                on_click=lambda e: fechar_ficha(),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=14,
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
    )

    def obter_dados_formulario():
        return (
            nome_field.value.strip(),
            cpf_field.value.strip(),
            nascimento_field.value.strip(),
            telefone_field.value.strip(),
            email_field.value.strip(),
            endereco_field.value.strip(),
            cidade_field.value.strip(),
            observacoes_field.value.strip(),
            ultima_consulta_field.value.strip(),
        )

    def preparar_formulario_para_edicao(dados_paciente):
        nonlocal paciente_editando_id
        paciente_editando_id = dados_paciente[0]
        nome_field.value = dados_paciente[1] or ""
        cpf_field.value = _formatar_cpf(dados_paciente[2]) if dados_paciente[2] else ""
        nascimento_field.value = _formatar_data(dados_paciente[3]) if dados_paciente[3] else ""
        telefone_field.value = _formatar_telefone(dados_paciente[4]) if dados_paciente[4] else ""
        email_field.value = dados_paciente[5] or ""
        endereco_field.value = dados_paciente[6] or ""
        cidade_field.value = dados_paciente[7] or ""
        observacoes_field.value = dados_paciente[8] or ""
        ultima_consulta_field.value = dados_paciente[9] or ""
        form_title_text.value = "Editar paciente"
        submit_button.text = "Atualizar paciente"
        submit_button.icon = ft.Icons.SAVE_AS
        status_text.value = f"Editando {dados_paciente[1] or 'paciente'}"
        status_text.color = ft.Colors.BLUE_700
        status_text.visible = True
        page.update()

    def limpar_formulario(e=None):
        nonlocal paciente_editando_id
        for _, field in campos:
            field.value = ""
        paciente_editando_id = None
        form_title_text.value = "Cadastro de Paciente"
        submit_button.text = "Salvar paciente"
        submit_button.icon = ft.Icons.SAVE_AS
        status_text.value = ""
        status_text.visible = False
        page.update()

    # Funções de apoio
    def fechar_ficha(e=None):
        modal_layer.visible = False
        page.update()

    def abrir_ficha(e, dados_paciente):
        nome = dados_paciente[1] if dados_paciente[1] else "Paciente"
        cpf = _formatar_cpf(dados_paciente[2]) if len(dados_paciente) > 2 and dados_paciente[2] else "Não informado"
        nascimento = _formatar_data(dados_paciente[3]) if len(dados_paciente) > 3 and dados_paciente[3] else "Não informado"
        telefone = _formatar_telefone(dados_paciente[4]) if len(dados_paciente) > 4 and dados_paciente[4] else "Não informado"
        email = dados_paciente[5] if len(dados_paciente) > 5 and dados_paciente[5] else "Não informado"
        endereco = dados_paciente[6] if len(dados_paciente) > 6 and dados_paciente[6] else "Não informado"
        cidade = dados_paciente[7] if len(dados_paciente) > 7 and dados_paciente[7] else "Não informado"
        observacoes = dados_paciente[8] if len(dados_paciente) > 8 and dados_paciente[8] else "Nenhuma observação registrada"
        ultima_consulta = _formatar_texto_data(dados_paciente[9]) if len(dados_paciente) > 9 else "Não tem última consulta"

        modal_title.value = nome
        modal_info.controls = [
            ft.Row(controls=[ft.Text("CPF", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(cpf, color=ft.Colors.GREY_900)], spacing=8),
            ft.Row(controls=[ft.Text("Data de nascimento", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(nascimento, color=ft.Colors.GREY_900)], spacing=8),
            ft.Row(controls=[ft.Text("Telefone", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(telefone, color=ft.Colors.GREY_900)], spacing=8),
            ft.Row(controls=[ft.Text("E-mail", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(email, color=ft.Colors.GREY_900)], spacing=8),
            ft.Row(controls=[ft.Text("Endereço", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(endereco, color=ft.Colors.GREY_900)], spacing=8),
            ft.Row(controls=[ft.Text("Cidade", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(cidade, color=ft.Colors.GREY_900)], spacing=8),
            ft.Row(controls=[ft.Text("Última consulta", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(ultima_consulta, color=ft.Colors.GREY_900)], spacing=8),
        ]
        modal_observacoes.controls = [
            ft.Text("Observações médicas", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text(observacoes, selectable=True, color=ft.Colors.GREY_800),
        ]
        modal_layer.visible = True
        page.update()

    # Eventos de máscara
    def on_cpf_change(e):
        cpf_field.value = _formatar_cpf(e.control.value)
        cpf_field.update()

    def on_data_change(e):
        nascimento_field.value = _formatar_data(e.control.value)
        nascimento_field.update()

    def on_telefone_change(e):
        telefone_field.value = _formatar_telefone(e.control.value)
        telefone_field.update()

    cpf_field.on_change = on_cpf_change
    nascimento_field.on_change = on_data_change
    telefone_field.on_change = on_telefone_change

    # Carregamento e renderização
    def carregar_pacientes():
        lista_pacientes.controls.clear()
        pacientes = buscar_pacientes()

        if not pacientes:
            lista_pacientes.controls.append(
                ft.Container(
                    content=ft.Text("Nenhum paciente cadastrado no momento.", size=16, color=ft.Colors.GREY_700),
                    padding=ft.Padding.only(left=20, right=20, top=20, bottom=20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=12,
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                )
            )
        else:
            for paciente in pacientes:
                paciente_id = paciente[0]
                nome = paciente[1] if paciente[1] else "Paciente"
                cpf = _formatar_cpf(paciente[2]) if len(paciente) > 2 and paciente[2] else "Não informado"
                nascimento = _formatar_data(paciente[3]) if len(paciente) > 3 and paciente[3] else "Não informado"
                telefone = _formatar_telefone(paciente[4]) if len(paciente) > 4 and paciente[4] else "Não informado"
                ultima_consulta = _formatar_texto_data(paciente[9]) if len(paciente) > 9 else "Não tem última consulta"

                lista_pacientes.controls.append(
                    ft.Container(
                        padding=14,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=14,
                        border=ft.Border.all(1, ft.Colors.GREY_200),
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=42,
                                            height=42,
                                            border_radius=21,
                                            bgcolor=ft.Colors.BLUE_50,
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_700),
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(nome, size=15, weight=ft.FontWeight.BOLD),
                                                ft.Text(telefone, size=12, color=ft.Colors.GREY_600),
                                            ],
                                            expand=True,
                                            spacing=2,
                                        ),
                                        ft.Container(
                                            content=ft.Text("Ativo", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                                            bgcolor=ft.Colors.GREEN_600,
                                            border_radius=20,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=12,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(f"CPF: {cpf}", size=13, color=ft.Colors.GREY_700),
                                        ft.Text(f"Nasc.: {nascimento}", size=13, color=ft.Colors.GREY_700),
                                        ft.Text(f"Últ. consulta: {ultima_consulta}", size=13, color=ft.Colors.GREY_700),
                                    ],
                                    spacing=16,
                                    wrap=True,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            ft.Icons.VISIBILITY_OUTLINED,
                                            icon_color=ft.Colors.BLUE_600,
                                            on_click=lambda e, p=paciente: abrir_ficha(e, p),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.EDIT_OUTLINED,
                                            icon_color=ft.Colors.BLUE_600,
                                            on_click=lambda e, p=paciente: preparar_formulario_para_edicao(p),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_600,
                                            on_click=lambda e, p=paciente: (excluir_paciente(p[0]), status_text.update(), carregar_pacientes(), page.update()),
                                        ),
                                    ],
                                    spacing=2,
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=8,
                        ),
                    )
                )

        page.update()

    def salvar_paciente(e=None):
        nonlocal paciente_editando_id
        campos_vazios = [label for label, field in campos if not str(field.value or "").strip()]
        if campos_vazios:
            status_text.value = f"Preencha todos os campos obrigatórios: {', '.join(campos_vazios)}"
            status_text.color = ft.Colors.RED_600
            status_text.visible = True
            page.update()
            return

        dados = obter_dados_formulario()
        if paciente_editando_id is None:
            inserir_paciente(dados)
            status_text.value = "Paciente salvo com sucesso!"
            status_text.color = ft.Colors.GREEN_700
        else:
            atualizar_paciente(paciente_editando_id, dados)
            status_text.value = "Paciente atualizado com sucesso!"
            status_text.color = ft.Colors.BLUE_700
            paciente_editando_id = None

        limpar_formulario()
        status_text.visible = True
        carregar_pacientes()
        page.update()

    # Blocos da interface
    form_title_text = ft.Text("Cadastro de Paciente", size=20, weight=ft.FontWeight.BOLD)
    form_subtitle_text = ft.Text("Preencha as informações para registrar um novo paciente", size=13, color=ft.Colors.GREY_600)
    submit_button = ft.ElevatedButton(
        "Salvar paciente",
        icon=ft.Icons.SAVE_AS,
        on_click=salvar_paciente,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    form_card = ft.Container(
        width=520,
        padding=24,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        border=ft.Border.all(1, ft.Colors.GREY_200),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_200, offset=ft.Offset(0, 6), spread_radius=1),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PERSON_ADD_ALT_1, color=ft.Colors.BLUE_600, size=24),
                        ft.Column(
                            controls=[
                                form_title_text,
                                form_subtitle_text,
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(color=ft.Colors.GREY_200),
                ft.Row(controls=[nome_field, cpf_field], spacing=12),
                ft.Row(controls=[nascimento_field, telefone_field], spacing=12),
                ft.Row(controls=[email_field, endereco_field], spacing=12),
                ft.Row(controls=[cidade_field, ultima_consulta_field], spacing=12),
                observacoes_field,
                status_text,
                ft.Row(
                    controls=[
                        submit_button,
                        ft.OutlinedButton(
                            "Limpar formulário",
                            icon=ft.Icons.CLEAR,
                            on_click=limpar_formulario,
                            style=ft.ButtonStyle(
                                color=ft.Colors.RED_600,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=14,
        ),
    )

    list_card = ft.Container(
        expand=True,
        padding=24,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        border=ft.Border.all(1, ft.Colors.GREY_200),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_200, offset=ft.Offset(0, 6), spread_radius=1),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Pacientes cadastrados", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Gerencie a base de pacientes da clínica", size=13, color=ft.Colors.GREY_600),
                            ],
                            spacing=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.TextField(
                    expand=True,
                    hint_text="Buscar por nome, CPF ou telefone",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=12,
                    border_color=ft.Colors.GREY_300,
                    filled=True,
                    bgcolor=ft.Colors.GREY_50,
                    dense=True,
                    content_padding=ft.Padding.only(left=12, right=12, top=14, bottom=14),
                ),
                lista_pacientes,
            ],
            spacing=14,
        ),
    )

    carregar_pacientes()

    main_content = ft.Container(
        expand=True,
        padding=20,
        bgcolor=ft.Colors.GREY_50,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Pacientes", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text("Cadastre, visualize e gerencie os pacientes da clínica", size=15, color=ft.Colors.GREY_600),
                            ],
                            spacing=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[form_card, list_card],
                    spacing=20,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=20,
        ),
    )

    return ft.Stack(
        expand=True,
        controls=[main_content, modal_layer],
    )
