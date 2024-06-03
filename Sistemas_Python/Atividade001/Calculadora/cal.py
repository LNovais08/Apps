import flet  as ft

def main(page: ft.Page): # Função para criar a pagina
    page.title = "Calculadora" # Titulo
    result = ft.Text(value="0") # Area onde vai mostrar o resultado

    page.add(
        ft.Row(controls=[result]), #ft.Row coloca os itens em linhas
        ft.Row(
            controls=[
                        ft.ElevatedButton(text="A"),
                        ft.ElevatedButton(text="+/-"),
                        ft.ElevatedButton(text="%"),
                        ft.ElevatedButton(text="÷"),
            ]
        ),
        
        ft.Row(
            controls=[
                        ft.ElevatedButton(text="7 "),
                        ft.ElevatedButton(text=" 8 "),
                        ft.ElevatedButton(text=" 9"),
                        ft.ElevatedButton(text=" x "),
            ]
        ),


        ft.Row(
            controls=[
                        ft.ElevatedButton(text="4 "),
                        ft.ElevatedButton(text=" 5 "),
                        ft.ElevatedButton(text= "6"),
                        ft.ElevatedButton(text=" -  "),
            ]
        ),
        
        ft.Row(
            controls=[
                        ft.ElevatedButton(text="1 "),
                        ft.ElevatedButton(text=" 2 "),
                        ft.ElevatedButton(text=" 3"),
                        ft.ElevatedButton(text=" + "),
            ]
        ),

        ft.Row(
            controls=[
                        ft.ElevatedButton(text="0"),
                        ft.ElevatedButton(text="."),
                        ft.ElevatedButton(text="=", width=140),
            ]
        ),

    )

ft.app(target=main)