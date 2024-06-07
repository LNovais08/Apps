from flet import *
import flet as ft

def main(page: ft.Page):
    # Função para criar a pagina
    page.title = "Calculadora"  # Titulo
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    result = ft.Text(value="0", color="black", size=24)  # Área onde vai mostrar o resultado
    current_input = ""

    def update_display(value):
        result.value = value
        page.update()

    def button_click(e):
        nonlocal current_input
        text = e.control.text

        if text == "A":
            current_input = ""
        elif text == "=":
            try:
                current_input = str(eval(current_input.replace("x", "*").replace("÷", "/")))
            except Exception as ex:
                current_input = "Erro"
        else:
            current_input += text

        update_display(current_input)

    linha0 = ft.Row(controls=[result], alignment=ft.MainAxisAlignment.CENTER)  # ft.Row coloca os itens em linhas

    linha1 = ft.Row(
        controls=[
            ft.ElevatedButton(text="A", on_click=button_click),
            ft.ElevatedButton(text="+/-", on_click=button_click),
            ft.ElevatedButton(text="%", on_click=button_click),
            ft.ElevatedButton(text="÷", on_click=button_click),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    linha2 = ft.Row(
        controls=[
            ft.ElevatedButton(text="7", on_click=button_click),
            ft.ElevatedButton(text="8", on_click=button_click),
            ft.ElevatedButton(text="9", on_click=button_click),
            ft.ElevatedButton(text="x", on_click=button_click),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=18
    )

    linha3 = ft.Row(
        controls=[
            ft.ElevatedButton(text="4", on_click=button_click),
            ft.ElevatedButton(text="5", on_click=button_click),
            ft.ElevatedButton(text="6", on_click=button_click),
            ft.ElevatedButton(text="-", on_click=button_click),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=18
    )

    linha4 = ft.Row(
        controls=[
            ft.ElevatedButton(text="1", on_click=button_click),
            ft.ElevatedButton(text="2", on_click=button_click),
            ft.ElevatedButton(text="3", on_click=button_click),
            ft.ElevatedButton(text="+", on_click=button_click),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=18
    )

    linha5 = ft.Row(
        controls=[
            ft.ElevatedButton(text="0", on_click=button_click),
            ft.ElevatedButton(text=".", on_click=button_click),
            ft.ElevatedButton(text="=", width=140, on_click=button_click),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=17
    )

    div = ft.Container(
        content=ft.Column(
            controls=[linha0, linha1, linha2, linha3, linha4, linha5],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        bgcolor=ft.colors.WHITE,
        width=350,
        height=400,
        border_radius=15,
        alignment = ft.alignment.center
    )

    page.add(div)

ft.app(target=main)
