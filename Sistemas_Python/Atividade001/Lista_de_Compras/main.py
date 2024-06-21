from flet import *
import flet as ft
import sqlite3

def main(page: Page):
    # Definindo o título da página
    page.title = "Lista de Compras"

    # Função para conectar ao banco de dados e criar as tabelas se não existirem
    def init_db():
        conn = sqlite3.connect('Atividade001/Lista_de_Compras/db/compras.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS compras
                          (idLista TEXT, idCompra INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)''')
        conn.commit()
        conn.close()

    # Inicializa o banco de dados
    init_db()

    # Obtém o último id_lista ou cria um novo se não existir
    def get_current_id_lista():
        conn = sqlite3.connect('Atividade001/Lista_de_Compras/db/compras.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idLista) FROM compras")
        result = cursor.fetchone()
        if result[0] is None:
            id_lista = 0
        else:
            id_lista = int(result[0]) + 1
        conn.close()
        return id_lista

    # Contador de itens
    cont = 0
    id_lista = get_current_id_lista()
    item_list = []

    # Função para adicionar item à lista
    def add_item(e):
        nonlocal cont  # Permite modificar a variável cont
        item = compra.value.strip()
        if item:
            # Incrementa o contador e adiciona o item na lista
            cont += 1
            item_list.append(item)
            linhaLV = create_item_row(cont, item)
            items.controls.append(linhaLV)
            compra.value = ""
            items.update()
            page.update()
        else:
            compra.error_text = "Item não pode ser vazio"
            compra.update()

    def create_item_row(index, item):
        item_text = ft.Text(f"{index}. {item}", size=20, color="black")
        edit_button = ft.IconButton(icon=ft.icons.EDIT_ROUNDED, icon_color="green")
        delete_button = ft.IconButton(icon=ft.icons.DELETE_SHARP, icon_color="red")

        edit_button.on_click = lambda e: edit_item(e, index-1)
        delete_button.on_click = lambda e: delete_item(e, index-1)

        return ft.Row(
            controls=[
                item_text,
                ft.Row(
                    controls=[edit_button, delete_button],
                    spacing=0
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )

    def delete_item(e, index):
        item_list.pop(index)
        refresh_list()

    def edit_item(e, index):
        def close_dlg(e):
            edited_text = edit_text.value.strip()
            if edited_text:
                item_list[index] = edited_text
                refresh_list()
            dlg.open = False
            page.update()

        edit_text = ft.TextField(label="Digite aqui", value=item_list[index])
        dlg = ft.AlertDialog(
            actions=[
                edit_text,
                ft.TextButton(text="OK", on_click=close_dlg),
            ],
            actions_padding=10,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()


    def refresh_list():
        items.controls.clear()
        for i, item in enumerate(item_list):
            items.controls.append(create_item_row(i + 1, item))
        items.update()
        page.update()

    # Função para finalizar a lista e salvar os itens no banco de dados
    def Fim(e):
        nonlocal id_lista, cont
        if items.controls:
            # Conecta ao banco de dados e insere os valores
            conn = sqlite3.connect('Atividade001/Lista_de_Compras/db/compras.db')
            cursor = conn.cursor()
            for item in item_list:  # Pegar os itens da lista pelo for
                cursor.execute("INSERT INTO compras (idLista, nome) VALUES (?, ?)", (id_lista, item))  # Insere os itens no db

            conn.commit()
            conn.close()
            items.controls.clear()  # Limpa a lista
            item_list.clear()
            items.update()
            page.update()
            cont = 0  # Reinicia o contador
            # Incrementa o id_lista para a próxima lista
            id_lista = get_current_id_lista()

    # Lista de itens
    items = ft.ListView(expand=True, spacing=10)

    # Itens que contém na página
    text_login = ft.Text("Lista de Compras", color="black", size=35)
    compra = ft.TextField(label="Comprar", color="black", height=35)
    add = ft.FilledTonalButton(text="Adicionar", icon="add", height=35, on_click=add_item)
    final = ft.FilledTonalButton(text="Finalizar", icon="library_add_check_rounded", height=35, on_click=Fim)

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
            controls=[text_login, linha, items, final],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        bgcolor=ft.colors.WHITE,
        width=595,
        height=670,
        alignment=ft.alignment.center
    )
    principal.content = ft.Row(
        controls=[img_lista, lista],
        alignment=ft.MainAxisAlignment.CENTER,  # Centralizando os contêineres na tela
        expand=True
    )

    page.add(principal)

ft.app(target=main)
