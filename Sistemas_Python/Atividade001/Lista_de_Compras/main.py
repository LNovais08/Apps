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
                          (idLista TEXT,idCompra INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)''')
        conn.commit()
        conn.close()

    # Inicializa o banco de dados
    init_db()

    # Obtém o último id_lista ou cria um novo se não existir
    def get_current_id_lista():
        conn = sqlite3.connect('Atividade001/Lista_de_Compras/db/compras.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idCompra) FROM compras")
        result = cursor.fetchone()
        if result[0] is None:
            cursor.execute("INSERT INTO compras DEFAULT VALUES")
            conn.commit()
            cursor.execute("SELECT MAX(idCompra) FROM compras")
            result = cursor.fetchone()
        conn.close()
        return result[0]

    # Contador de itens
    cont = 0
    id_lista = get_current_id_lista()

    # Função para adicionar item à lista
    def add_item(e):
        nonlocal cont  # Permite modificar a variável cont
        item = compra.value
        if item:
            # Incrementa o contador e adiciona o item na lista
            cont += 1
            items.controls.append(ft.Text(f"{cont}. {item}", size=20, color="black"))
            compra.value = ""
            items.update()
            page.update()

    # Função para finalizar a lista e salvar os itens no banco de dados
    def Fim(e):
        nonlocal id_lista, cont
        # Conecta ao banco de dados e insere os valores
        conn = sqlite3.connect('Atividade001/Lista_de_Compras/db/compras.db')
        cursor = conn.cursor()
        for control in items.controls:  # Pegar os itens da lista pelo for
            item_value = control.value.split(". ", 1)[1]  # Separa o número do item
            cursor.execute("INSERT INTO compras (idlista, nome) VALUES (?, ?)", (id_lista, item_value))  # Insere os itens no db
        conn.commit()
        conn.close()
        items.controls.clear()  # Limpa a lista
        items.update()
        page.update()
        cont = 0  # Reinicia o contador
        # Incrementa o id_lista para a próxima lista
        conn = sqlite3.connect('Atividade001/Lista_de_Compras/db/compras.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compras DEFAULT VALUES")
        conn.commit()
        id_lista = cursor.lastrowid
        conn.close()

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
