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
    # Funções de navegação
    def PDV(e):
        page.clean()
        def minus_click(e):
                txt_number.value = str(int(txt_number.value) - 1)
                page.update()

        def plus_click(e):
                txt_number.value = str(int(txt_number.value) + 1)
                page.update()
        
        # Itens para PDV
        Codigo = ft.TextField(label="Codigo", width=450, color="black", text_size=15)
        txt_number = ft.TextField(label="Qtd",value="0", text_align=ft.TextAlign.CENTER, width=50, color="black")
        mais = ft.ElevatedButton(
            text="+",
            width=60, 
            height=35,
            color="white", 
            style=ft.ButtonStyle(
                    shape={"": ft.RoundedRectangleBorder(radius=5)}  # Cantos retos
            ),
            on_click=plus_click

        )
        menos = ft.ElevatedButton(
            text="-", 
            width=60, 
            height=35, 
            color="white",
            style=ft.ButtonStyle(
                    shape={"": ft.RoundedRectangleBorder(radius=5)}  # Cantos retos
            ),
            on_click=minus_click                 
        )
         # Dados para exibir no DataGrid
        data = [
            ["John Doe", "john@example.com", "Admin"],
            ["Jane Smith", "jane@example.com", "User"],
            ["Sam Brown", "sam@example.com", "Guest"]
        ]

        # Definindo as colunas do DataGrid
        columns = [
            DataColumn(Text("Name")),
            DataColumn(Text("Email")),
            DataColumn(Text("Role"))
        ]

        # Adicionando as linhas de dados ao DataGrid
        rows = []
        for row_data in data:
            rows.append(DataRow(cells=[DataCell(Text(cell)) for cell in row_data]))

        # Criando o DataGrid com as colunas e linhas definidas
        data_grid = DataTable(columns=columns, rows=rows)
        principal = ft.Container(
                bgcolor=ft.colors.WHITE,
                alignment=ft.alignment.center,
                expand=True
        )
        principal.content = ft.Row(
            controls=[Codigo, txt_number, mais, menos,data_grid],
            alignment=ft.MainAxisAlignment.CENTER,  # Centralizando os contêineres na tela
            expand=True
        )
        page.add(principal)
        page.update()

    def CadastroU(e):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Text("Cadastro Usuário!", size=30, color=ft.colors.BLACK),
            )
        )
        page.update()

    def CadastroP(e):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Text("Cadastro Produto", size=30, color=ft.colors.BLACK),
            )
        )
        page.update()

    def Vendas(e):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Text("Vendas", size=30, color=ft.colors.BLACK),
            )
        )
        page.update()
    def Voltar(e):
        page.clean()
        page.add(background_image)
        page.update()
    # Barra de aplicativos com menu de popup
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
