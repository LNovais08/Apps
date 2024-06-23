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
        page.add(
            ft.Container(
                content=ft.Text("Cadastro Usuário!", size=30, color=ft.colors.BLACK),
                alignment=ft.alignment.center,
                expand=True
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
