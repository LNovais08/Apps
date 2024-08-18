from flet import *
import flet as ft
import sqlite3
import json
import unidecode
import datetime
import csv
import pandas as pd
import matplotlib.pyplot as plt


class App:

    def  __init__(self, page: Page):
        self.page = page
        self.page.title = "SuperMarket"
        # Centralizar a janela na tela
        self.page.window_center()
        self.page.window_resizable = False
        self.page.padding = 40
        self.page.bgcolor = "WHITE"
        self.background_image = ft.Container(
            content=ft.Image(
                src="PDV/img/principal.jpg",  # Substitua pela URL da sua imagem de fundo
                fit=ft.ImageFit.COVER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            expand=True,
            visible=True  # Visível por padrão
        )
        self.current_page = None  # Armazenará a página atualmente visível

        # Ler as informações do usuário do arquivo temporário
        with open("temp_user_info.json", "r") as temp_file:
            user_info = json.load(temp_file)

        # Barra de aplicativos com menu
        menu_items = [
            ft.PopupMenuItem(text="PDV", icon="MONETIZATION_ON", on_click=self.show_pdv),
            ft.PopupMenuItem(text="Home", icon="HOME", on_click=self.show_home)
        ]

        if user_info['grau'] == "Admin":
            menu_items.extend([
                ft.PopupMenuItem(text="Cadastro Usuário", icon="APP_REGISTRATION", on_click=self.show_cadastro_usuario),
                ft.PopupMenuItem(text="Cadastro Produto", icon="APP_REGISTRATION", on_click=self.show_cadastro_produto),
                ft.PopupMenuItem(text="Vendas", icon="SELL", on_click=self.show_vendas)
            ])
        # Barra de aplicativos com menu
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.STORAGE),
            leading_width=40,
            title=ft.Text("SuperMarket"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.PopupMenuButton(
                    items=menu_items
                ),
            ],
        )

        # Mostra a página inicial ao iniciar o aplicativo
        self.show_home(None)

    #MOSTRAR AS PAGINAS DE FORMA CORRETA
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
    
    #CRIANDO A PAGINA PDV
    def create_pdv_page(self):
        # Exemplo de criação da página PDV
        items = []

        def update_total():
            if desconto_value.value != "00.00%":
                total = sum(float(row[2]) * float(row[3]) for row in items) - float(desconto_value.value.replace("%", ''))
                total_text.value = f"Total: R$ {total:.2f}"
            else:
                total = sum(float(row[2]) * float(row[3]) for row in items)
                total_text.value = f"Total: R$ {total:.2f}"
            self.page.update()

        def add_to_list(e):
            if Codigo.value and Produto.value and txt_valor.value and txt_number.value.isdigit():
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('PDV/db/cadastrosU.db')
                cursor = conn.cursor()

                produto = unidecode.unidecode(Produto.value)
                qtd = txt_number.value
                # Atualiza a quantidade no estoque para cada item vendido
            
                # Primeiro, recupera a quantidade atual do estoque
                cursor.execute("SELECT Quantidade FROM Estoque WHERE Produto = ?", (produto,))
                quantidade_atual = cursor.fetchone()

                if quantidade_atual:

                    if int(qtd) >= int(quantidade_atual[0]):
                        def close_modal(e):
                            modal.open = False
                            self.page.update()
                        modal = ft.AlertDialog(
                            modal=True,
                            title=ft.Text("Não Temos Estoque"),
                            actions=[
                                ft.TextButton("OK", on_click=close_modal),
                            ],
                            actions_alignment=ft.MainAxisAlignment.END
                        )
                        self.page.dialog = modal
                        modal.open = True
                        self.page.update()

                    else:
                                
                        items.append([Codigo.value, Produto.value, txt_number.value, txt_valor.value])
                        update_table()
                        Codigo.value = ""
                        Produto.value = ""
                        txt_number.value = ""
                        txt_valor.value = ""
                        self.page.update()
                        update_total()

                        nova_quantidade = int(quantidade_atual[0]) - int(qtd)

                        # Atualiza a quantidade no banco de dados
                        sql = f"UPDATE Estoque SET Quantidade = {nova_quantidade} WHERE Produto = '{produto}'"
                        print(sql)
                        cursor.execute(sql)
                else:
                    print(f"Produto {produto} não encontrado no estoque.")

                conn.commit()
                conn.close()
                self.page.update()
        
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
                now = datetime.datetime.now()
                # Formata a data e hora como string
                data = now.strftime("%Y-%m-%d")
                User1 = caixa_value.value
                Cliente1 = cpf_value.value
                Compras = [unidecode.unidecode(item[1]) for item in items]  # Pega todos os valores da coluna "Produto"
                Compras1 = json.dumps(Compras)
                Valor1 = total_text.value.replace("Total: R$ ", '').strip()
                Data1 = data
                Estado1 = "Pago"
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                # Insere os dados de venda
                cursor.execute("INSERT INTO Vendas (User, Cliente, Compras, Valor_Total, Data, Estado) VALUES (?, ?, ?, ?, ?, ?)", 
                            (User1, Cliente1, Compras1, Valor1, Data1, Estado1))

                conn.commit()
                conn.close()
                Codigo.value = ""
                Produto.value = ""
                txt_number.value = ""
                txt_valor.value = ""
                total_text.value = ""
                items.clear()
                update_table()
                n_nota_label.value = ids()
                cpf_value.value = ""
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
                User1 = caixa_value.value
                Cliente1 = cpf_value.value
                Compras = [unidecode.unidecode(item[1]) for item in items]   # Pega todos os valores da coluna "Produto"
                Compras1 = json.dumps(Compras)
                Valor1 = total_text.value
                Data1 = data
                Estado1 = "Cancelado"
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Vendas (User, Cliente, Compras, Valor_Total, Data, Estado) VALUES (?, ?, ?, ?, ?, ?)", (User1, Cliente1,Compras1, Valor1, Data1, Estado1))
                conn.commit()
                conn.close()
                Codigo.value = ""
                Produto.value = ""
                txt_number.value = ""
                txt_valor.value = ""
                total_text.value = ""
                items.clear()
                update_table()
                n_nota_label.value = ids()
                cpf_value.value = ""
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
        def ids():
            # Conecta ao banco de dados e obtém o último id
            conn = sqlite3.connect('PDV/db/cadastrosU.db')
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
            return id1
        # Obtém a data e hora atuais
        now = datetime.datetime.now()
        # Formata a data e hora como string
        data = now.strftime("%d/%m/%Y")
        hora = now.strftime("%H:%M")
        # Define the contents of the labels
        n_nota = ft.Text(value="N° da Nota", size=25, font_family="Times New Roman", color="black")
        n_nota_label = ft.Text(value=ids(), size=18, color="black")

        data_label = ft.Text(value="Data: ", size=20, font_family="Times New Roman", color="black")
        data_value = ft.Text(value=data, size=18, color="black")
        hora_label = ft.Text(value="Hora: ", size=20, font_family="Times New Roman", color="black")
        hora_value = ft.Text(value=hora, size=19, color="black")

        cpf_label = ft.Text(value="CPF: ", size=20, font_family="Times New Roman", color="black")

        def format_cpf(e):
            # Remove non-digit characters and limit to 11 characters
            raw_cpf = ''.join(filter(str.isdigit, cpf_value.value))[:11]

            # Format the CPF
            formatted_cpf = raw_cpf
            if len(raw_cpf) > 9:
                formatted_cpf = f"{raw_cpf[:3]}.{raw_cpf[3:6]}.{raw_cpf[6:9]}-{raw_cpf[9:11]}"
            elif len(raw_cpf) > 6:
                formatted_cpf = f"{raw_cpf[:3]}.{raw_cpf[3:6]}.{raw_cpf[6:]}"
            elif len(raw_cpf) > 3:
                formatted_cpf = f"{raw_cpf[:3]}.{raw_cpf[3:]}"
            cpf_value.value = formatted_cpf
            self.page.update()

        def buscador(e):
            conn = sqlite3.connect('PDV/db/cadastrosU.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Vendas WHERE Cliente = ?", (cpf_value.value,))
            result = cursor.fetchone()[0]
            if result >= 5:
                # Concede o desconto
                desconto = 0.05  # 10% de desconto, por exemplo
                desconto_value.value = f"{desconto * 100}%"

            else:
                desconto_value.value = "00.00%"

            desconto_value.update()
            conn.close()
            
        cpf_value = ft.TextField(
            hint_text="Digite seu CPF...",
            color="black",
            width=200,
            height=80,
            text_size=23,
            max_length=14,
            on_change=format_cpf,
            border_radius=0,
            border_color="transparent",
            filled=True, 
            bgcolor=ft.colors.GREY_300,
            on_blur=buscador
        )
        
        with open("temp_user_info.json", "r") as temp_file:
            user_info = json.load(temp_file)
        
        caixa_label = ft.Text(value="Caixa: ", size=20, font_family="Times New Roman", color="black")
        caixa_value = ft.Text(value=user_info['id'], size=19, color="black")

        estado_label = ft.Text(value="Estado: ", size=20, font_family="Times New Roman", color="black")
        estado_value = ft.Text(value=user_info['grau'], size=19, color="black")

        desconto_label = ft.Text(value="Desconto: ", size=20, font_family="Times New Roman", color="black")
        desconto_value = ft.Text(value="00.00%", size=19, color="black")
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
        content=ft.Row(
            [cpf_label, cpf_value],
            spacing=5,
            alignment=ft.MainAxisAlignment.END,  # Align items to the right within the row
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Ensure vertical alignment in the center
        ),
        alignment=ft.alignment.center_right,
        padding=ft.padding.all(5)
        )
        div5 = ft.Container(
            content=ft.Column([caixa_label, caixa_value], spacing=10, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        div6 = ft.Container(
            content=ft.Column([estado_label, estado_value], spacing=10, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        div7 = ft.Container(
            content=ft.Column([desconto_label, desconto_value], spacing=10, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        # Create the main navigation container
        nave = ft.Container(
            content=ft.Row([div1, div2, div3, div4, div5, div6, div7], spacing=20, alignment=ft.alignment.center),
            alignment=ft.alignment.center,
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

    #CRIANDO CADASTRO DE USUARIOS
    def create_cadastro_usuario_page(self):

        def link_clicked(e):
            nome1 = nome.value
            tel1 = tel.value
            email1 = email.value
            sexo1 = sexo.value
            senha1 = senha.value
            adm1 = adm.value
            if not email1:
                email.error_text = "Preencha seu E-mail"
                self.page.update()
            elif not senha1:
                senha.error_text = "Preencha sua Senha"
                self.page.update()
            elif not nome1:
                nome.error_text = "Preencha seu Nome"
                self.page.update()
            elif not sexo1:
                sexo.error_text = "Preencha qual o seu Sexo"
                self.page.update()
            elif not tel1:
                tel.error_text = "Preencha seu Telefone"
                self.page.update()
            else:
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cadastros_Usuarios (nome, Tel, email, sexo, grau, senha) VALUES (?, ?, ?, ?, ?, ?)", (nome1, tel1, email1, sexo1, adm1, senha1))
                conn.commit()
                conn.close()
                nome.value = ""
                tel.value = ""
                email.value = ""
                sexo.value = ""
                adm.value = ""
                senha.value = ""
                self.page.update()
        
        # Função para formatar e validar o telefone
        def format_telefone(e):
            raw_tel = ''.join(filter(str.isdigit, tel.value))[:11]  # Somente dígitos e max 11 caracteres
            formatted_tel = raw_tel
            if len(raw_tel) > 10:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:7]}-{raw_tel[7:11]}"
            elif len(raw_tel) > 6:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:6]}-{raw_tel[6:]}"
            elif len(raw_tel) > 2:
                formatted_tel = f"({raw_tel[:2]}) {raw_tel[2:]}"
            tel.value = formatted_tel
            self.page.update()

        def dropdown_changed(e):
            adm.value = adm.value
            self.page.update()

        
        # Itens para Cadastro de Usuário
        nome = ft.TextField(
            label="Nome",
            width=450,
            color="black",
            text_size=18,
            border_color="black",
            border_radius=5,
            label_style=ft.TextStyle(color="black"),
        )

        tel = ft.TextField(
            label="Telefone",
            width=450,
            color="black",
            text_size=18,
            border_color="black",
            border_radius=5,
            label_style=ft.TextStyle(color="black"),
            on_change=format_telefone
        )

        email = ft.TextField(
            label="E-mail",
            text_align=ft.TextAlign.CENTER,
            width=450,
            color="black",
            border_color="black",
            border_radius=5,
            label_style=ft.TextStyle(color="black"),
        )

        sexo = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="Feminino", label="Feminino",label_style=ft.TextStyle(color="black"),),
                    ft.Radio(value="Masculino", label="Masculino",label_style=ft.TextStyle(color="black"),)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        )

        adm = ft.Dropdown(
            width=450,
            on_change=dropdown_changed,
            options=[
                ft.dropdown.Option("Admin", text_style=ft.TextStyle(color="black")),
                ft.dropdown.Option("Funcionário", text_style=ft.TextStyle(color="black")),
            ],
            border_radius=5,
            border_color="black",
        )

        senha = ft.TextField(
            label="Senha",
            width=450,
            color="black",
            password=True,
            can_reveal_password=True,
            text_size=18,
            border_color="black",
            border_radius=5,
            label_style=ft.TextStyle(color="black"),
        )

        # Botão de Cadastro
        cadastrar_button = ft.ElevatedButton(
            text="Cadastrar",
            on_click=link_clicked,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=10)},
                color="white",
                bgcolor="black"
            ),
            width=250,
            height=50
        )

        # Layout do formulário
        cadastrou = ft.Column(
            controls=[nome, tel, email, sexo, adm, senha, cadastrar_button],
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
            bgcolor="rgba(0, 0, 0, 0.5)",
            alignment=ft.alignment.center
        )


            
        bg = ft.Stack(
                controls=[
                    ft.Image(
                        src="PDV/img/CD.jpg",  # Substitua pela URL da sua imagem de fundo
                        fit=ft.ImageFit.COVER,
                        expand=True,
                        width= 20000,
                    ),
                    form_container  # O formulário sobrepõe a imagem de fundo
                ],
                alignment=ft.alignment.center,
                expand=True
            )
        return bg
    
    #CRIANDO CADASTRO DE PRODUTOS
    def create_cadastro_produto_page(self):
        def link_clicked(e):
            # Obtém a data e hora atuais
            now = datetime.datetime.now()
            # Formata a data e hora como string
            data = now.strftime("%d/%m/%Y")
            produto1 = unidecode.unidecode(produto.value)
            valor_unit1 = valor_unit.value
            qtd1 = qtd.value
            Validade1 = Validade.value
            if not produto1:
                produto.error_text = "Preencha o Nome do Produto"
                self.page.update()
            elif not valor_unit1:
                valor_unit.error_text = "Preencha o Valor Unitário"
                self.page.update()
            elif not Validade1:
                Validade.error_text = "Preencha a Data de Validade"
                self.page.update()
            elif not qtd1:
                qtd.error_text = "Preencha a Quantidade"
                self.page.update()
            else:
                # Conecta ao banco de dados e insere os valores
                conn = sqlite3.connect('PDV/db/cadastrosU.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Estoque (Produto, Valor_Unitario, Quantidade, Data, Validade) VALUES (?, ?, ?, ?, ?)", (produto1, valor_unit1, qtd1, data, Validade1))
                conn.commit()
                conn.close()
                produto.value = ""
                valor_unit.value = ""
                qtd.value = ""
                Validade.value = "Nenhuma DATA selecionada"
                self.page.update()
        

        # Itens para Cadastro de Usuário
        produto = ft.TextField(
            label="Produto",
            width=450,
            color="black",
            text_size=18,
            border_color="black",
            border_radius=5,
        )

        valor_unit = ft.TextField(
            label="Valor Unitário",
            text_align=ft.TextAlign.CENTER,
            width=450,
            color="black",
            border_color="black",
            border_radius=5,
        )

        qtd = ft.TextField(
            label="Quantidade",
            width=450,
            text_align=ft.TextAlign.CENTER,
            color="black",
            text_size=18,
            border_color="black",
            border_radius=5,
        )

        def handle_date_change(e: ft.ControlEvent):
            Validade.value = f"Data Selecionada: {e.control.value.strftime('%Y-%m-%d')}"
            self.page.update()

        def handle_dismissal(e):
            Validade.value = f"Data Não selecionada"

        # Botão para abrir o DatePicker
        ValidadeD = ft.ElevatedButton(
            "Data",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                    on_change=handle_date_change,
                    on_dismiss=handle_dismissal,
                )
            ),
        )
        
        # Label para exibir a data selecionada
        Validade = ft.Text("Nenhuma DATA selecionada", color="Black")

        # Linha com a data e o botão
        linha = ft.Row(
            controls=[Validade, ValidadeD],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=10
        )

        # Botão de Cadastro
        cadastrar_button = ft.ElevatedButton(
            text="Cadastrar",
            on_click=link_clicked,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=10)},
                color="white",
                bgcolor="black"
            ),
            width=250,
            height=50,
        )

        # Layout do formulário
        cadastrou = ft.Column(
            controls=[produto, valor_unit, qtd, linha, cadastrar_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20  # Espaçamento vertical entre os controles na coluna
        )

        # Contêiner principal com estilos
        form_container = ft.Container(
            content=cadastrou,
            width=500,
            padding=20,
            margin=20,
            border_radius=10,
            bgcolor="rgba(0, 0, 0, 0.5)",
            alignment=ft.alignment.center
        )

        bg = ft.Stack(
                controls=[
                    ft.Image(
                        src="PDV/img/CD.jpg",  # Substitua pela URL da sua imagem de fundo
                        fit=ft.ImageFit.COVER,
                        expand=True,
                        width= 20000,
                    ),
                    form_container  # O formulário sobrepõe a imagem de fundo
                ],
                alignment=ft.alignment.center,
                expand=True
            )
        return bg

    #CRIANDO CADASTRO DE VENDAS
    def create_vendas_page(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('PDV/db/cadastrosU.db')
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute("SELECT Valor_Total, Data, Estado FROM Vendas")
        vendas_data = cursor.fetchall()
        conn.close()

        # Salvar os dados em um arquivo CSV
        with open('vendas_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Valor_Total", "Data", "Estado"])  # Cabeçalhos
            writer.writerows(vendas_data)

        # Ler os dados do CSV
        df = pd.read_csv("vendas_data.csv", sep=",", decimal=".")
        df["Data"] = pd.to_datetime(df["Data"])
        df = df.sort_values("Data")

        # Adicionar uma coluna de mês para filtro
        df["Month"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

        # Criar um gráfico de linha para mostrar a evolução do valor total ao longo do tempo
        plt.figure(figsize=(10, 6))
        plt.plot(df['Data'], df['Valor_Total'])
        plt.xlabel('Data')
        plt.ylabel('Valor Total')
        plt.title('Evolução do Valor Total ao Longo do Tempo')
        # Salve o gráfico em um arquivo
        plt.savefig('PDV/img/grafico.png')
        return ft.Image(
            src='PDV/img/grafico.png',
            width=800,
            height=600,
        )

ft.app(target=App)
