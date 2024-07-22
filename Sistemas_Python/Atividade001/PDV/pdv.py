from flet import *
import flet as ft
import sqlite3
from datetime import datetime
import json
import unidecode
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart


class App:

    def  __init__(self, page: Page):
        self.page = page
        self.page.title = "SuperMarket"
        self.page.window_resizable = False
        self.page.padding = 40
        self.page.bgcolor = "WHITE"
        self.background_image = ft.Container(
            content=ft.Image(
                src="Atividade001/PDV/img/principal.jpg",  # Substitua pela URL da sua imagem de fundo
                fit=ft.ImageFit.COVER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            expand=True,
            visible=True  # Visível por padrão
        )
        self.current_page = None  # Armazenará a página atualmente visível

        # Barra de aplicativos com menu
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.STORAGE),
            leading_width=40,
            title=ft.Text("SuperMarket"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="PDV", icon="MONETIZATION_ON", on_click=self.show_pdv),
                        ft.PopupMenuItem(text="Cadastro Usuário", icon="APP_REGISTRATION", on_click=self.show_cadastro_usuario),
                        ft.PopupMenuItem(text="Cadastro Produto", icon="APP_REGISTRATION", on_click=self.show_cadastro_produto),
                        ft.PopupMenuItem(text="Vendas", icon="SELL", on_click=self.show_vendas),
                        ft.PopupMenuItem(text="Home", icon="HOME", on_click=self.show_home)
                    ]
                ),
            ],
        )

        # Mostra a página inicial ao iniciar o aplicativo
        self.show_home(None)

    def show_pdv(self, e):
        self.hide_background_image()
        if self.current_page:
            self.page.controls.remove(self.current_page)  # Remove a página atual
            self.current_page.visible = False  # Esconde a página atual, se existir
        self.current_page = self.create_pdv_page()
        self.page.add(self.current_page)
        self.page.update()

    def show_cadastro_usuario(self, e):
        self.hide_background_image()
        if self.current_page:
            self.page.controls.remove(self.current_page)  # Remove a página atual
            self.current_page.visible = False
        self.current_page = self.create_cadastro_usuario_page()
        self.page.add(self.current_page)
        self.page.update()

    def show_cadastro_produto(self, e):
        self.hide_background_image()
        if self.current_page:
            self.page.controls.remove(self.current_page)  # Remove a página atual
            self.current_page.visible = False
        self.current_page = self.create_cadastro_produto_page()
        self.page.add(self.current_page)
        self.page.update()

    def show_vendas(self, e):
        self.hide_background_image()
        if self.current_page:
            self.page.controls.remove(self.current_page)  # Remove a página atual
            self.current_page.visible = False
        self.current_page = self.create_vendas_page()
        self.page.add(self.current_page)
        self.page.update()

    def show_home(self, e):
        if self.current_page:
            self.page.controls.remove(self.current_page)  # Remove a página atual
            self.current_page.visible = False  # Esconde a página atual, se existir
            self.current_page = None
        if self.background_image not in self.page.controls:
            self.page.controls.append(self.background_image)  # Adiciona a camada de fundo de volta
        self.page.update()

    def hide_background_image(self):
        if self.background_image in self.page.controls:
            self.page.controls.remove(self.background_image)
            self.page.update()
    
    def create_pdv_page(self):
        # Exemplo de criação da página PDV
        items = []

        def update_total():
            total = sum(float(row[2]) * float(row[3]) for row in items)
            total_text.value = f"Total: R$ {total:.2f}"
            self.page.update()

        def add_to_list(e):
            if Codigo.value and Produto.value and txt_valor.value and txt_number.value.isdigit():
                items.append([Codigo.value, Produto.value, txt_number.value, txt_valor.value])
                update_table()
                Codigo.value = ""
                Produto.value = ""
                txt_number.value = ""
                txt_valor.value = ""
                self.page.update()
                update_total()
        
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
            self.page.update()

        def pagar(e):
            selected_payment = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value="cartao", label="Cartão"),
                    ft.Radio(value="dinheiro", label="Dinheiro"),
                    ft.Radio(value="pix", label="Pix"),
                ], width=300)  # Define a largura do grupo de rádio
            )

            def on_ok_click(e):
                # Mostrar outro modal com a opção de pagamento selecionada
                second_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirmar Pagamento"),
                    content=ft.Text(f"Forma de Pagamento escolhida: {selected_payment.value}"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: close_second_modal(second_modal)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                self.page.dialog = second_modal
                second_modal.open = True
                self.page.update()

            def close_second_modal(modal):
                modal.open = False
                # Obtém a data e hora atuais
                now = datetime.now()
                # Formata a data e hora como string
                data = now.strftime("%Y-%m-%d")
                User1 = "Lais"
                Compras = [unidecode.unidecode(item[1]) for item in items]  # Pega todos os valores da coluna "Produto"
                Compras1 = json.dumps(Compras)
                Valor1 = total_text.value
                Data1 = data
                Estado1 = "Pago"
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Vendas (User, Compras, Valor_Total, Data, Estado) VALUES (?, ?, ?, ?, ?)", (User1, Compras1, Valor1, Data1, Estado1))
                conn.commit()
                conn.close()
                Codigo.value = ""
                Produto.value = ""
                txt_number.value = ""
                txt_valor.value = ""
                total_text.value = ""
                items.clear()
                self.page.update()

            modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Escolha o modo de Pagamento!"),
                content=ft.Column(
                    controls=[
                        ft.Text("Forma de Pagamento -> Cartão, Dinheiro ou Pix"),
                        selected_payment
                    ],
                    width=300, 
                    height=150  
                ),
                actions=[
                    ft.TextButton("OK", on_click=on_ok_click),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            self.page.dialog = modal
            modal.open = True
            self.page.update()


        def cancelar(e):


            def on_ok_click(e):
                # Mostrar outro modal com a opção de pagamento selecionada
                second_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirmar Cancelamento"),
                    content=ft.Text(f"Sua Compra está sendo cancelada..."),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: close_second_modal(second_modal)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                self.page.dialog = second_modal
                second_modal.open = True
                self.page.update()

            def close_second_modal(modal):
                modal.open = False
                # Obtém a data e hora atuais
                now = datetime.now()
                # Formata a data e hora como string
                data = now.strftime("%Y-%m-%d %H:%M:%S")
                User1 = "Lais"
                Compras = [unidecode.unidecode(item[1]) for item in items]   # Pega todos os valores da coluna "Produto"
                Compras1 = json.dumps(Compras)
                Valor1 = total_text.value
                Data1 = data
                Estado1 = "Cancelado"
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Vendas (User, Compras, Valor_Total, Data, Estado) VALUES (?, ?, ?, ?, ?)", (User1, Compras1, Valor1, Data1, Estado1))
                conn.commit()
                conn.close()
                Codigo.value = ""
                Produto.value = ""
                txt_number.value = ""
                txt_valor.value = ""
                total_text.value = ""
                items.clear()
                update_table()
                self.page.update()

            modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Você está cancelando sua compra!"),
                actions=[
                    ft.TextButton("OK", on_click=on_ok_click),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            self.page.dialog = modal
            modal.open = True
            self.page.update()
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
        # Conecta ao banco de dados e obtém o último id
        conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM Vendas")
        result = cursor.fetchone()
        conn.close()
        # Se result for None, significa que não há registros na tabela. Então, definimos id como 0.
        if result[0] is None:
            id = 0
        else:
            id = int(result[0])  # Certifique-se de que id seja um inteiro
        # Incrementa o id
        id1 = id + 1
        id1 = str(id1).zfill(12)
        # Obtém a data e hora atuais
        now = datetime.now()
        # Formata a data e hora como string
        data = now.strftime("%d/%m/%Y")
        hora = now.strftime("%H:%M:%S")
        # Define the contents of the labels
        n_nota = ft.Text(value="N° da Nota", size=25, font_family="Times New Roman", color="black")
        n_nota_label = ft.Text(value=str(id1), size=18, color="black")

        data_label = ft.Text(value="Data: ", size=20, font_family="Times New Roman", color="black")
        data_value = ft.Text(value=data, size=18, color="black")
        hora_label = ft.Text(value="Hora: ", size=20, font_family="Times New Roman", color="black")
        hora_value = ft.Text(value=hora, size=19, color="black")

        cpf_label = ft.Text(value="CPF: ", size=20, font_family="Times New Roman", color="black")
        cpf_value = ft.TextField(color="black", width=157, height=40, text_size=20)

        # Create containers for each div with proper styling and spacing
        div1 = ft.Container(
            content=ft.Column([n_nota, n_nota_label]),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        div2 = ft.Container(
            content=ft.Column([data_label, data_value], spacing=10, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        div3 = ft.Container(
            content=ft.Column([hora_label, hora_value], spacing=10, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        div4 = ft.Container(
            content=ft.Row([cpf_label, cpf_value], spacing=10, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        # Create the main navigation container
        nave = ft.Container(
            content=ft.Row([div1, div2, div3, div4], spacing=20, alignment=ft.alignment.center),
            alignment=ft.alignment.top_center,
            padding=ft.padding.all(10),
            bgcolor=ft.colors.GREY_300,
            height=120,
            border_radius=ft.border_radius.all(10)
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
        data_grid = DataTable(
            columns=columns,
            rows=[],
            width=800,
            border=ft.border.all(2, "black"),
            show_bottom_border=True,
        )

        cv = ft.Column([data_grid], scroll=True)
        rv = ft.Row([cv], scroll=True, expand=1, vertical_alignment=ft.CrossAxisAlignment.START)

        linha1 = ft.Row(
            controls=[Codigo, Produto, txt_number, txt_valor, adicionar],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
        linha2 = ft.Container(
            content=rv,
            alignment=ft.alignment.top_center,  # Alinhar ao topo central
            expand=True
        )

        # Contêiner adicional para contador e botões
        total_text = ft.Text("Total: R$ 0.00", size=20, color=ft.colors.BLACK)
        pagar_button = ft.ElevatedButton(
            text="Pagar",
            width=120,
            height=35,
            color="white",
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=5)}
            ),
            on_click=pagar
        )
        cancelar_button = ft.ElevatedButton(
            text="Cancelar",
            width=120,
            height=35,
            color="white",
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=5)}
            ),
            on_click=cancelar
        )
        linha3 = ft.Row(
            controls=[total_text, pagar_button, cancelar_button],
            alignment=ft.MainAxisAlignment.CENTER
        )

        principal = ft.Container(
            content=ft.Column(
                controls=[nave, linha1, linha2, linha3],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Alinhamento espaçado
                expand=True
            ),
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            expand=True
        )
        return principal

    def create_cadastro_usuario_page(self):
        # Exemplo de criação da página de Cadastro de Usuário

        def link_clicked(e):
            nome1 = Nome.value
            tel1 = Tel.value
            email1 = Email.value
            sexo1 = sexo.value
            senha1 = senha.value
            adm1 = adm.value
            if not email1:
                Email.error_text = "Preencha seu E-mail"
                self.page.update()
            elif not senha1:
                senha.error_text = "Preencha sua Senha"
                self.page.update()
            elif not nome1:
                Nome.error_text = "Preencha seu Nome"
                self.page.update()
            elif not sexo1:
                sexo.error_text = "Preencha qual o seu Sexo"
                self.page.update()
            elif not tel1:
                Tel.error_text = "Preencha seu Telefone"
                self.page.update()
            else:
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cadastros_Usuarios (nome, Tel, email, sexo, grau, senha) VALUES (?, ?, ?, ?, ?, ?)", (nome1, tel1, email1, sexo1, adm1, senha1))
                conn.commit()
                conn.close()
                Nome.value = ""
                Tel.value = ""
                Email.value = ""
                sexo.value = ""
                adm.value = ""
                senha.value = ""
                self.page.update()
        
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
            self.page.update()

        def dropdown_changed(e):
            adm.value = adm.value
            self.page.update()

        
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
        adm = ft.Dropdown(
            width=450,
            on_change=dropdown_changed,
            options=[
                ft.dropdown.Option("Admin"),
                ft.dropdown.Option("Funcionário"),
            ],
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
            controls=[Nome, Tel, Email, sexo, adm, senha, cadastrar_button],
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

        return ft.Container(
            content=form_container,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.BLUE_GREY_50,
        )

    def create_cadastro_produto_page(self):
        # Exemplo de criação da página de Cadastro de Produto
        return ft.Container(
            content=ft.Text("Cadastro Produto", size=30, color=ft.colors.BLACK),
            alignment=ft.alignment.center,
            expand=True
        )

    def create_vendas_page(self):
        conn = sqlite3.connect('Atividade001/PDV/db/cadastrosU.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Valor_Total, Data FROM Vendas")
        vendas_data = cursor.fetchall()
        conn.close()

        valores = [row[0] for row in vendas_data]
        datas = [row[1] for row in vendas_data]

        fig, ax = plt.subplots()
        ax.plot(datas, valores)
        ax.set_title('Vendas')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor Total')

        chart = MatplotlibChart(fig, expand=True)

        return ft.Container(
            content=chart,
            alignment=ft.alignment.center,
            expand=True
        )
ft.app(target=App)
