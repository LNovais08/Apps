import sys
from cx_Freeze import setup, Executable
 
# Definir se o aplicativo é gráfico ou console
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Para aplicativos gráficos, como Flet
 
# Detalhes do seu aplicativo
executables = [Executable("login.py", base=base)]
 
# Opções do cx_Freeze
options = {
    "build_exe": {
        "packages": [],  # Pacotes adicionais se necessário
        "include_files": [
            "db/",        # Inclui a pasta 'telas'
            "img/",  # Inclui a pasta 'formularios'
            "principal/"        # Inclui a pasta 'banco'
        ]
    }
}
 
# Configuração do cx_Freeze
setup(
    name="PDV",
    version="1.0",
    description="Gerenciar provisões e estornos da Expresso Nepomuceno",
    options=options,
    executables=executables
)