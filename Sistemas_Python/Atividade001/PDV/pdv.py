from flet import *
import flet as ft
import sqlite3

def main(page: Page):
    
    # título da Barra
    page.title = "SuperMarket"
    # proibindo o redimensionamento da Tela
    page.window_resizable = False
    # alinhamento da view
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # vertical
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER # horizontal
    # padding da page
    page.padding = 40
    page.bgcolor = "WHITE"
    # Variáveis globais
    items = []

    # Função para conectar ao banco de dados e criar a tabela se não existir
    def init_db():
        conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cadastros_Usuarios
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, Tel TEXT, email TEXT, sexo TEXT, senha TEXT)''')
        conn.commit()
        conn.close()

    # Inicializa o banco de dados
    init_db()

    # Funções de navegação
    def PDV(e):
        page.clean()
        
        def add_to_list(e):
            if Codigo.value and Produto.value and txt_valor.value and txt_number.value.isdigit():
                items.append([Codigo.value, Produto.value, txt_number.value, txt_valor.value])
                update_table()
                Codigo.value = ""
                Produto.value = ""
                txt_number.value = ""
                txt_valor.value = ""
                page.update()
        
        def delete_item(index):
            def delete_click(e):
                items.pop(index)
                update_table()
            return delete_click
        
        def edit_item(index):
            def edit_click(e):
                Codigo.value, Produto.value, txt_number.value, txt_valor.value = items[index]
                items.pop(index)
                update_table()
            return edit_click
        
        def update_table():
            rows = []
            for index, row in enumerate(items):
                row_color = ft.colors.GREY_200 if index % 2 == 0 else ft.colors.GREY_400
                rows.append(DataRow(
                    cells=[
                        DataCell(Text(cell, color=ft.colors.BLACK)) for cell in row
                    ] + [
                        DataCell(
                            Row(
                                controls=[
                                    IconButton(icon=ft.icons.DELETE, on_click=delete_item(index), icon_color="red"),
                                    IconButton(icon=ft.icons.EDIT, on_click=edit_item(index), icon_color="green")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    ],  
                    color=row_color
                ))
            data_grid.rows = rows
            page.update()

        # Itens para PDV
        Codigo = ft.TextField(label="Código", width=150, color="black", text_size=15)
        Produto = ft.TextField(label="Produto", width=450, color="black", text_size=15)
        txt_number = ft.TextField(label="Qtd", text_align=ft.TextAlign.CENTER, width=60, color="black")
        txt_valor = ft.TextField(label="Valor", text_align=ft.TextAlign.CENTER, width=150, color="black")

        adicionar = ft.ElevatedButton(
            text="Adicionar",
            width=120,
            height=55,
            color="white",
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=5)}  # Cantos retos
            ),
            on_click=add_to_list
        )
        
        # Definindo as colunas do DataGrid
        columns = [
            DataColumn(Text("Código", color=ft.colors.BLACK)),
            DataColumn(Text("Produto", color=ft.colors.BLACK)),
            DataColumn(Text("Quantidade", color=ft.colors.BLACK)),
            DataColumn(Text("Valor Unitário", color=ft.colors.BLACK)),
            DataColumn(Text("", color=ft.colors.BLACK))
        ]
        
        # Criando o DataGrid com as colunas definidas
        data_grid = DataTable(columns=columns, 
                              rows=[],
                              width=1000,
                              border=ft.border.all(2, "black"),
                              show_bottom_border=True,
                    )
        cv = ft.Column([data_grid],scroll=True)
        rv = ft.Row([cv],scroll=True,expand=1,vertical_alignment=ft.CrossAxisAlignment.START)

        linha1 = ft.Row(
            controls=[Codigo, Produto, txt_number, txt_valor, adicionar],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
        linha2 = ft.Container(
            content=rv,
            alignment=ft.alignment.top_center,  # Align top center horizontal alignment
            expand=True
        )
        principal = ft.Container(
            content=ft.Column(
                controls=[linha1, linha2],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Align start 
                expand=True
            ),
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            expand=True
        )
        page.add(principal)
        page.update()

    def CadastroU(e):
        page.clean()

        def link_clicked(e):
            nome1 = Nome.value
            tel1 = Tel.value
            email1 = Email.value
            sexo1 = sexo.value
            senha1 = senha.value
            if not email1:
                Email.error_text = "Preencha seu E-mail"
                page.update()
            elif not senha1:
                senha.error_text = "Preencha sua Senha"
                page.update()
            elif not nome1:
                Nome.error_text = "Preencha seu Nome"
                page.update()
            elif not sexo1:
                sexo.error_text = "Preencha qual o seu Sexo"
                page.update()
            elif not tel1:
                Tel.error_text = "Preencha seu Telefone"
                page.update()
            else:
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cadastros_Usuarios (nome, Tel, email, sexo, senha) VALUES (?, ?, ?, ?, ?)", (nome1, tel1, email1, sexo1, senha1))
                conn.commit()
                conn.close()
                Nome.value = ""
                Tel.value = ""
                Email.value = ""
                sexo.value = ""
                senha.value = ""
                page.update()
        
        # Função para formatar e validar o telefone
        def format_telefone(e):
            raw_tel = ''.join(filter(str.isdigit, Tel.value))[:11]  # Somente dígitos e max 11 caracteres
            formatted_tel = raw_tel
            if len(raw_tel) > 10:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:7]}-{raw_tel[7:11]}"
            elif len(raw_tel) > 6:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:6]}-{raw_tel[6:]}"
            elif len(raw_tel) > 2:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:]}"
            Tel.value = formatted_tel
            page.update()

        # Itens para Cadastro de Usuário
        Nome = ft.TextField(label="Nome", width=450, color="black", text_size=15, border_color="gray")
        Tel = ft.TextField(label="Telefone", width=450, color="black", text_size=15, border_color="gray", on_change=format_telefone)
        Email = ft.TextField(label="E-mail", text_align=ft.TextAlign.CENTER, width=450, color="black", border_color="gray")
        sexo = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="Feminino", label="Feminino"),
                ft.Radio(value="Masculino", label="Masculino")
            ], alignment=ft.MainAxisAlignment.CENTER),
        ) 
        senha = ft.TextField(label="Senha", width=450, color="black", password=True, can_reveal_password=True, text_size=15, border_color="gray")
        
        # Botão de Cadastro
        cadastrar_button = ft.ElevatedButton(
            text="Cadastrar",
            on_click=link_clicked,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=5)},
                color="white",
                bgcolor="gray"
            ),
            width=200,
            height=50,
        )
    
        # Layout do formulário
        cadastrou = ft.Column(
            controls=[Nome, Tel, Email, sexo, senha, cadastrar_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        # Contêiner principal com estilos
        form_container = ft.Container(
            content=cadastrou,
            width=500,
            padding=20,
            margin=20,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color="black",
                offset=ft.Offset(5, 5),
                spread_radius=1,
            ),
            alignment=ft.alignment.center,
        )

        # Adicionando o contêiner à página
        page.add(
            ft.Container(
                content=form_container,
                alignment=ft.alignment.center,
                expand=True,
                image_src="Atividade001/PDV/img/Foto.jpg",
                image_fit=ft.ImageFit.COVER,
            )
        )
        page.update()

    def CadastroP(e):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Text("Cadastro Produto", size=30, color=ft.colors.BLACK),
                alignment=ft.alignment.center,
                expand=True
            )
        )
        page.update()

    def Vendas(e):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Text("Vendas", size=30, color=ft.colors.BLACK),
                alignment=ft.alignment.center,
                expand=True
            )
        )
        page.update()

    def Voltar(e):
        page.clean()
        page.add(background_image)
        page.update()

    # Barra de aplicativos com menu
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.STORAGE),
        leading_width=40,
        title=ft.Text("SuperMarket"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="PDV", icon="MONETIZATION_ON", on_click=PDV),
                    ft.PopupMenuItem(text="Cadastro Usuário", icon="APP_REGISTRATION", on_click=CadastroU),
                    ft.PopupMenuItem(text="Cadastro Produto", icon="APP_REGISTRATION", on_click=CadastroP),
                    ft.PopupMenuItem(text="Vendas", icon="SELL", on_click=Vendas),
                    ft.PopupMenuItem(text="Home", icon="OUTBOND", on_click=Voltar)
                ]
            ),
        ],
    )

    # Definindo o fundo da página com um Container que contém a imagem de fundo
    background_image = ft.Image(
        src="Atividade001/PDV/img/principal.jpg",  # Substitua pela URL da sua imagem
        fit=ft.ImageFit.COVER,
        expand=True
    )

    page.add(background_image)
    page.update()

ft.app(target=main)
