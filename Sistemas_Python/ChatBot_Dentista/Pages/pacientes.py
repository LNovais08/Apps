import sqlite3
import re
from pathlib import Path
import flet as ft
import requests
from database import ensure_schema


def _get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "db" / "clinica.db"


def _normalizar_paciente(paciente) -> dict:
    if isinstance(paciente, dict):
        return paciente

    if not paciente:
        return {
            "id": None,
            "nome": "",
            "cpf": "",
            "data_nascimento": "",
            "telefone": "",
            "email": "",
            "endereco": "",
            "cidade": "",
            "observacoes_medicas": "",
            "cep": "",
            "numero": "",
            "uf": "",
            "data_cadastro": "",
        }

    return {
        "id": paciente[0],
        "nome": paciente[1] or "",
        "cpf": paciente[2] or "",
        "data_nascimento": paciente[3] or "",
        "telefone": paciente[4] or "",
        "email": paciente[5] or "",
        "endereco": paciente[6] or "",
        "cidade": paciente[7] or "",
        "observacoes_medicas": paciente[8] or "",
        "cep": paciente[9] or "",
        "numero": paciente[10] or "",
        "uf": paciente[11] or "",
        "data_cadastro": paciente[12] if len(paciente) > 12 else "",
    }


def buscar_pacientes():
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, nome, cpf, data_nascimento, telefone, email, endereco, cidade, observacoes_medicas, cep, numero, uf, data_cadastro
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
            nome, cpf, data_nascimento, telefone, email, endereco, cidade, observacoes_medicas, cep, numero, uf
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        SET nome = ?, cpf = ?, data_nascimento = ?, telefone = ?, email = ?, endereco = ?, cidade = ?, observacoes_medicas = ?, cep = ?, numero = ?, uf = ?
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


def _formatar_cep(valor: str) -> str:
    numeros = re.sub(r"\D", "", valor or "")[:8]
    if len(numeros) <= 5:
        return numeros
    return f"{numeros[:5]}-{numeros[5:]}"


def _email_valido(valor: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", (valor or "").strip()))


def build_pacientes_page(page: ft.Page):
    nome_field = _campo_formulario("Nome completo", ft.Icons.PERSON_OUTLINE)
    cpf_field = _campo_formulario("CPF", ft.Icons.BADGE_OUTLINED, max_length=14)
    nascimento_field = _campo_formulario("Data de nascimento", ft.Icons.CALENDAR_TODAY, max_length=10)
    telefone_field = _campo_formulario("Telefone", ft.Icons.PHONE_ANDROID, max_length=15)
    email_field = _campo_formulario("E-mail", ft.Icons.EMAIL_OUTLINED)
    cep_field = _campo_formulario("CEP", ft.Icons.MAP_OUTLINED, max_length=9)
    endereco_field = _campo_formulario("Endereço", ft.Icons.HOME_OUTLINED)
    numero_field = _campo_formulario("Número", ft.Icons.HOUSE_OUTLINED)
    cidade_field = _campo_formulario("Cidade", ft.Icons.LOCATION_ON_OUTLINED)
    uf_field = _campo_formulario("UF", ft.Icons.FLAG_OUTLINED, max_length=2)
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
        ("CEP", cep_field),
        ("Endereço", endereco_field),
        ("Número", numero_field),
        ("Cidade", cidade_field),
        ("UF", uf_field),
        ("Observações médicas", observacoes_field),
    ]

    status_text = ft.Text("", visible=False, color=ft.Colors.GREEN_700)
    lista_pacientes = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
    paciente_editando_id = None

    modal_title = ft.Text("", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    modal_subtitle = ft.Text("Dados cadastrais completos", size=12, color=ft.Colors.GREY_600)
    modal_info = ft.Column(controls=[], spacing=8, scroll=ft.ScrollMode.AUTO)
    modal_observacoes = ft.Column(controls=[], spacing=4)
    modal_layer = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.BLACK_26,
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=560,
            padding=24,
            bgcolor=ft.Colors.GREY_100,
            border_radius=24,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_300, offset=ft.Offset(0, 2), spread_radius=0),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=50,
                                height=50,
                                border_radius=25,
                                bgcolor=ft.Colors.BLUE_100,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_700, size=24),
                            ),
                            ft.Column(
                                controls=[
                                    modal_title,
                                    modal_subtitle,
                                ],
                                spacing=1,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=ft.Colors.GREY_200),
                    ft.Container(
                        padding=12,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=14,
                        content=modal_info,
                    ),
                    ft.Container(
                        padding=14,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=14,
                        content=modal_observacoes,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Fechar",
                                icon=ft.Icons.CLOSE,
                                on_click=lambda e: fechar_ficha(),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_600,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
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
            cep_field.value.strip(),
            numero_field.value.strip(),
            uf_field.value.strip(),
        )

    def preparar_formulario_para_edicao(dados_paciente):
        nonlocal paciente_editando_id
        paciente_data = _normalizar_paciente(dados_paciente)
        paciente_editando_id = paciente_data["id"]
        nome_field.value = paciente_data["nome"] or ""
        cpf_field.value = _formatar_cpf(paciente_data["cpf"]) if paciente_data["cpf"] else ""
        nascimento_field.value = _formatar_data(paciente_data["data_nascimento"]) if paciente_data["data_nascimento"] else ""
        telefone_field.value = _formatar_telefone(paciente_data["telefone"]) if paciente_data["telefone"] else ""
        email_field.value = paciente_data["email"] or ""
        endereco_field.value = paciente_data["endereco"] or ""
        cidade_field.value = paciente_data["cidade"] or ""
        observacoes_field.value = paciente_data["observacoes_medicas"] or ""
        cep_field.value = paciente_data["cep"] or ""
        numero_field.value = paciente_data["numero"] or ""
        uf_field.value = paciente_data["uf"] or ""
        form_title_text.value = "Editar paciente"
        submit_button.text = "Atualizar paciente"
        submit_button.icon = ft.Icons.SAVE_AS
        status_text.value = f"Editando {paciente_data['nome'] or 'paciente'}"
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

    def buscar_cep(e=None):
        cep = re.sub(r"\D", "", cep_field.value or "")
        if len(cep) != 8:
            return

        try:
            resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=10)
            resposta.raise_for_status()
            dados_cep = resposta.json()
            if dados_cep.get("erro"):
                return

            endereco_field.value = dados_cep.get("logradouro", "") or ""
            cidade_field.value = dados_cep.get("localidade", "") or ""
            uf_field.value = dados_cep.get("uf", "") or ""
            status_text.value = "Endereço preenchido automaticamente."
            status_text.color = ft.Colors.GREEN_700
            status_text.visible = True
            page.update()
        except Exception:
            return

    def fechar_ficha(e=None):
        modal_layer.visible = False
        page.update()

    def abrir_ficha(e, dados_paciente):
        paciente_data = _normalizar_paciente(dados_paciente)
        nome = paciente_data["nome"] or "Paciente"
        cpf = _formatar_cpf(paciente_data["cpf"]) if paciente_data["cpf"] else "Não informado"
        nascimento = _formatar_data(paciente_data["data_nascimento"]) if paciente_data["data_nascimento"] else "Não informado"
        telefone = _formatar_telefone(paciente_data["telefone"]) if paciente_data["telefone"] else "Não informado"
        email = paciente_data["email"] or "Não informado"
        endereco = paciente_data["endereco"] or "Não informado"
        cidade = paciente_data["cidade"] or "Não informado"
        observacoes = paciente_data["observacoes_medicas"] or "Nenhuma observação registrada"
        cep = paciente_data["cep"] or "Não informado"
        numero = paciente_data["numero"] or "Não informado"
        uf = paciente_data["uf"] or "Não informado"

        modal_title.value = nome
        modal_info.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Informações pessoais", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Row(controls=[ft.Text("CPF", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(cpf, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("Data de nascimento", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(nascimento, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("Telefone", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(telefone, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("E-mail", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(email, color=ft.Colors.GREY_900)], spacing=8),
                    ],
                    spacing=4,
                ),
                padding=0,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Endereço", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Row(controls=[ft.Text("CEP", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(cep, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("Endereço", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(endereco, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("Número", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(numero, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("Cidade", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(cidade, color=ft.Colors.GREY_900)], spacing=8),
                        ft.Row(controls=[ft.Text("UF", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700), ft.Text(uf, color=ft.Colors.GREY_900)], spacing=8),
                    ],
                    spacing=4,
                ),
                padding=0,
            ),
        ]
        modal_observacoes.controls = [
            ft.Text("Observações médicas", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text(observacoes, selectable=True, color=ft.Colors.GREY_800),
        ]
        modal_layer.visible = True
        page.update()

    def on_cpf_change(e):
        cpf_field.value = _formatar_cpf(e.control.value)
        cpf_field.update()

    def on_data_change(e):
        nascimento_field.value = _formatar_data(e.control.value)
        nascimento_field.update()

    def on_telefone_change(e):
        telefone_field.value = _formatar_telefone(e.control.value)
        telefone_field.update()

    def on_cep_change(e):
        cep_field.value = _formatar_cep(e.control.value)
        cep_field.update()
        if len(re.sub(r"\D", "", cep_field.value or "")) == 8:
            buscar_cep()

    cpf_field.on_change = on_cpf_change
    nascimento_field.on_change = on_data_change
    telefone_field.on_change = on_telefone_change
    cep_field.on_change = on_cep_change

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
                paciente_data = _normalizar_paciente(paciente)
                nome = paciente_data["nome"] or "Paciente"
                cpf = _formatar_cpf(paciente_data["cpf"]) if paciente_data["cpf"] else "Não informado"
                nascimento = _formatar_data(paciente_data["data_nascimento"]) if paciente_data["data_nascimento"] else "Não informado"
                telefone = _formatar_telefone(paciente_data["telefone"]) if paciente_data["telefone"] else "Não informado"
                email = paciente_data["email"] or "Não informado"

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
                                                ft.Text(email, size=12, color=ft.Colors.GREY_600),
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

        if not _email_valido(email_field.value):
            status_text.value = "Informe um e-mail válido."
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
                ft.Row(controls=[email_field], spacing=12),
                ft.Row(controls=[cep_field, numero_field], spacing=12),
                ft.Row(controls=[cidade_field, uf_field], spacing=12),
                endereco_field,
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
                    hint_text="Buscar por nome, CPF, telefone ou e-mail",
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
