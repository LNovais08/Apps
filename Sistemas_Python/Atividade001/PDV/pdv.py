from flet import *
import flet as ft
import sqlite3

def main(page: Page):
    
    # título da Barra
    page.title = "Mercado"
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
        page.add(
            ft.Container(
                content=ft.Text("PDV!", size=30, color=ft.colors.BLACK),
            )
        )
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
        title=ft.Text("Mercado"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="PDV", icon="MONETIZATION_ON", on_click=PDV),
                    ft.PopupMenuItem(text="Cadastro Usuário", icon="APP_REGISTRATION", on_click=CadastroU),
                    ft.PopupMenuItem(text="Cadastro Produto", icon="APP_REGISTRATION", on_click=CadastroP),
                    ft.PopupMenuItem(text="Vendas", icon="SELL", on_click=Vendas),
                    ft.PopupMenuItem(text="Voltar", icon="OUTBOND", on_click=Voltar)
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
