from flet import *
import flet as ft
import sqlite3

def main(page: Page):
    # Definindo o título da página
    page.title = "Lista de Compras"


    # Função para adicionar item à lista
    def add_item(e):
        item = compra.value
        if item:
            # Adiciona o item na lista e atualiza a interface
            items.controls.append(ft.Text(item, size=20, color="black"))
            compra.value = ""
            page.update()
    
    # Lista de itens
    # Lista de itens
    items = ft.ListView(expand=True, spacing=10)

    # Itens que contem na pagina
    text_login = ft.Text("Lista de Compras", color="black", size=35)
    compra = ft.TextField(label="Comprar", color="black", height=35)
    add = ft.FilledTonalButton(text="Adicionar", icon="add", height=35, on_click=add_item)


    principal = Container(
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.center,
        expand=True
    )
    img_lista = Container(
        content=ft.Image(
            src='Atividade001/Lista_de_Compras/img/lista3.jpg',
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        expand=True,
    )
    linha = Container(
        content=ft.Row(
            controls=[compra, add],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    lista = Container(
        content=ft.Column(
                controls=[text_login, linha, items],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor=ft.colors.WHITE,
            width=595,
            height=670,
            alignment=ft.alignment.center
    )
    principal.content= ft.Row(
        controls=[img_lista, lista],
        alignment=ft.MainAxisAlignment.CENTER,  # Centralizando os contêineres na tela
        expand=True
    )
    page.add(principal)
ft.app(target=main)