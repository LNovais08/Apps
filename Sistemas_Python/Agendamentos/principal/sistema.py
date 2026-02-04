from flet import *
import flet as ft
import requests
import sqlite3
import os
import subprocess
import json
from datetime import datetime

def main(page: ft.Page):
    page.theme_mode = "light"
    page.title = "Agendamentos"
    page.window.center()
    page.padding = 0 
    page.window_resizable = False
    with open("temp_user_info.json", "r") as temp_file:
            user_info = json.load(temp_file)
    
    def atualizar_data():
        agora = datetime.now()
        return agora.strftime("%d/%m/%Y")

    def atualizar_hora():
        agora = datetime.now()
        return agora.strftime("%H:%M")
    
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
        page.update()

    def format_data(e):
        raw_data = ''.join(filter(str.isdigit, e.control.value))[:8]

        formatted_data = raw_data
        if len(raw_data) > 4:
            month = int(raw_data[2:4])
            if month < 1 or month > 12:
                e.control.error_text = "Mês inválido. Deve ser entre 01 e 12."
            else:
                e.control.error_text = None
            formatted_data = f"{raw_data[:2]}/{raw_data[2:4]}/{raw_data[4:]}"
        elif len(raw_data) > 2:
            formatted_data = f"{raw_data[:2]}/{raw_data[2:]}"

        e.control.value = formatted_data

        try:
            data_nascimento = datetime.strptime(formatted_data, "%d/%m/%Y")

            data_atual = datetime.now()
            idade = data_atual.year - data_nascimento.year

            if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
                idade -= 1
            
            idade_field.value = str(idade)
        except ValueError:
            idade_field.value = ""  

        e.page.update()

    def format_cep(e):
        # Remove non-digit characters and limit to 11 characters
        raw_cep = ''.join(filter(str.isdigit, e.control.value))[:8]

        # Format the CPF
        formatted_cpf = raw_cep
        if len(raw_cep) > 4:
            formatted_cpf = f"{raw_cep[:5]}-{raw_cep[5:8]}"
        e.control.value = formatted_cpf
        page.update()

    def format_cpf(e):
        # Remove non-digit characters and limit to 11 characters
        raw_cpf = ''.join(filter(str.isdigit, e.control.value))[:11]

        # Format the CPF
        formatted_cpf = raw_cpf
        if len(raw_cpf) > 9:
            formatted_cpf = f"{raw_cpf[:3]}.{raw_cpf[3:6]}.{raw_cpf[6:9]}-{raw_cpf[9:11]}"
        elif len(raw_cpf) > 6:
            formatted_cpf = f"{raw_cpf[:3]}.{raw_cpf[3:6]}.{raw_cpf[6:]}"
        elif len(raw_cpf) > 3:
            formatted_cpf = f"{raw_cpf[:3]}.{raw_cpf[3:]}"
        e.control.value = formatted_cpf
        page.update()

    def validate_cpf(e):
        cpF = e.control.value.replace('.', '').replace('-', '')
        if len(cpF) != 11 or not cpF.isdigit():
                return False
        soma1 = sum(int(digit) * weight for digit, weight in zip(cpF, range(10, 1, -1)))
        soma2 = sum(int(digit) * weight for digit, weight in zip(cpF, range(11, 1, -1)))
        resto1 = 11 - soma1 % 11
        resto2 = 11 - soma2 % 11
        if resto1 > 9:
                resto1 = 0
        if resto2 > 9:
                resto2 = 0
        resp = cpF[-2] == str(resto1) and cpF[-1] == str(resto2)
        if resp:
            print(cpF, "Valido")
        else:
            cpf.value = "CPF Inválido!!!"
            page.update()

    def buscar_cep(e):
        c = e.replace('-', '').strip()

        url = f"https://viacep.com.br/ws/{c}/json/" 
        response = requests.get(url) 
        if response.status_code == 200: 
            dados = response.json() 
            if "erro" not in dados: 
                return dados 
        return None

    def on_blur_endereco(e):
        cep = e.control.value
        end = buscar_cep(cep)
        
        if end:
            rua.value = end["logradouro"]
            cidade.value = end["localidade"]
            bairro.value = end["bairro"]
            estado.value = end["uf"]

        page.update()

    def on_blur_cpf(e):
        validate_cpf(e)

    #Páginas a serem EXIBIDAS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def pghome(e):
        paginas.controls.clear()
        paginas.update()
        paginas.controls.append(home)
        paginas.update()

    def pgconsultas(e):
        paginas.controls.clear()
        paginas.update()
        paginas.controls.append(consultas)
        paginas.update()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #HOME------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    video_bg = ft.Video(
        playlist=ft.VideoMedia(resource='img/PGinicial.mp4'),
        autoplay=True,
        show_controls=False,
        expand=True,
        fit=ft.ImageFit.COVER,
        playlist_mode='loop'
    )

    paginas = ft.Stack(
        expand=True,  
        controls=[video_bg],
    )

    home = ft.Container(
        content=video_bg
    )
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Itens para a consulta
    global idade_field
    cpf = ft.TextField(label="CPF", width=250, on_blur=on_blur_cpf,on_change=format_cpf, prefix_icon=ft.icons.PERSONAL_INJURY_OUTLINED)
    nome = ft.TextField(label="Nome", width=300, prefix_icon=ft.icons.PEOPLE_SHARP)
    tel = ft.TextField(label="Telefone", width=200, on_change=format_telefone, prefix_icon=ft.icons.PHONE)
    idade_field = ft.TextField(label="Idade", width=120, prefix_icon=ft.icons.NUMBERS, keyboard_type=ft.KeyboardType.NUMBER,read_only=True)
    data_nascimento = ft.TextField(label="Data de Nascimento", width=305, prefix_icon=ft.icons.CALENDAR_MONTH,keyboard_type=ft.KeyboardType.NUMBER,on_change=format_data)
    cep = ft.TextField(label="CEP", width=200, on_change=format_cep, on_blur=on_blur_endereco)
    rua = ft.TextField(label="Rua", width=420, prefix_icon=ft.icons.HOUSE, read_only=True)
    num = ft.TextField(label="Nº", width=130, prefix_icon=ft.icons.NUMBERS)
    estado = ft.TextField(label="UF", width=130, prefix_icon=ft.icons.FLAG, read_only=True)
    cidade = ft.TextField(label="Cidade", width=300, prefix_icon=ft.icons.LOCAL_ACTIVITY, read_only=True)
    bairro = ft.TextField(label="Bairro", width=320, prefix_icon=ft.icons.HOUSE, read_only=True)
    pc = ft.Column([
        ft.Text("Paciente", size=40, weight="bold"),
    ], 
        alignment=ft.MainAxisAlignment.START
    )
    linha1_paciente = ft.Row([nome,cpf,tel], alignment=ft.MainAxisAlignment.CENTER)
    linha2_paciente = ft.Row([idade_field,data_nascimento,
        ft.Dropdown(label="Convênio", width=325 , options=[
            ft.dropdown.Option("Unimed"),
            ft.dropdown.Option("SUS"),
            ft.dropdown.Option("Amil"),
            ft.dropdown.Option("SulAmérica"),
            ft.dropdown.Option("Bradesco"),
            ft.dropdown.Option("Vitallis"),
        ])
    ], alignment=ft.MainAxisAlignment.CENTER)
    linha3_paciente = ft.Row([cep,rua,num], alignment=ft.MainAxisAlignment.CENTER)
    linha4_paciente = ft.Row([estado,cidade,bairro], alignment=ft.MainAxisAlignment.CENTER)
    layout = ft.Column(
         controls=[pc,linha1_paciente,linha2_paciente,linha3_paciente,linha4_paciente]
    )

    paciente = ft.Container(
        content=layout,
        bgcolor="white",
        border_radius=10,
        width=850,
        height=650,
        alignment=ft.alignment.center,
        border=ft.border.all(1, ft.colors.BLACK),
    )
    consultas = ft.Container(
            bgcolor="#74bdce",
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[paciente],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
    )

    #NAVEBAR com os Botões --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    naveBar = Container(
        width=250,
        alignment=alignment.center_right,
        bgcolor="#4b9bb3",
        content=Column(  # Coluna para organizar os botões verticalmente
            controls=[
                ElevatedButton("Home", icon=icons.HOUSE, width=250, bgcolor="#4b9bb3", color="white", on_click=pghome),
                ElevatedButton("consultas", icon=icons.DOCUMENT_SCANNER_ROUNDED, width=250, bgcolor="#4b9bb3",color="white", on_click=pgconsultas),
                ElevatedButton("Relatórios", icon=icons.INFO, width=250, bgcolor="#4b9bb3",color="white"),
                ElevatedButton("Agendamentos", icon=icons.CALENDAR_MONTH, width=250, bgcolor="#4b9bb3",color="white"),
                ElevatedButton("Sair", icon=icons.EXIT_TO_APP, width=250, bgcolor="#4b9bb3",color="white"),
            ],
            alignment=alignment.center,
            spacing=10
        )
    )

    if user_info['grau'] != "adm":
         naveBar.content.controls.clear()
         naveBar.content.controls=[
              ElevatedButton("Home", icon=icons.HOUSE, width=250, bgcolor="#4b9bb3", color="white", on_click=pghome),
              ElevatedButton("Agendamentos", icon=icons.CALENDAR_MONTH, width=250, bgcolor="#4b9bb3",color="white"),
              ElevatedButton("Sair", icon=icons.EXIT_TO_APP, width=250, bgcolor="#4b9bb3",color="white"),
                           ]
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    main = Row(
        controls=[naveBar, paginas],
        expand=True,
        spacing=0
    )

    page.add(main)

ft.app(main)