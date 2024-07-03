<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.4/dist/sweetalert2.all.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.4/dist/sweetalert2.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.7.1.js" integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=" crossorigin="anonymous"></script>
    <!-- Option 1: Include in HTML -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <?php require_once("PDO/conexao.php") ?>
    <link rel="shortcut icon" type="" href="IMG/login-da-conta-financeira.png">
    <title>Login</title>
</head>
<style>
    body {
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background-image: url(IMG/bela-foto-de-uma-montanha-de-neve-ao-por-do-sol\ -\ Copia.png);
        background-repeat: no-repeat;
        background-size: cover;
    }

    .box {
        display: flex;
        width: 90vw;
        /* Alterado para ser responsivo */
        max-width: 1300px;
        height: 650px;
        /* Altura inicial */
        background: #ffffffc4;
        border-radius: 12px;
        box-shadow: rgba(0, 0, 0, 0.377) 0px 10px 20px, rgba(0, 0, 0, 0.521) 0px 6px 6px;
        transition: height 0.5s ease;
        /* Adicionado transição suave para a altura */
    }

    .left {
        display: flex;
        flex-direction: column;
        justify-items: center;
        align-items: center;
        background-image: url('IMG/foto.png');
        background-repeat: no-repeat;
        background-size: contain;
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
        flex: 1;
        /* Para ocupar toda a altura */
        position: relative;
        /* Adicionado para posicionar elementos filhos absolutamente */
    }

    #h1S {
        font-size: 5vw;
        /* Ajustado para ser responsivo */
        color: white;
        margin-left: 98px;
    }

    #h1L {
        font-size: 2vw;
        /* Ajustado para ser responsivo */
        margin-left: 100px;
        color: white;
        font-family: Georgia, 'Times New Roman', Times, serif;
    }

    #h2L {
        font-size: 1vw;
        /* Ajustado para ser responsivo */
        color: white;
        margin-left: 103px;
        font-family: "Times New Roman", Times, serif;
    }

    #h1lL {
        font-size: 3vw;
        /* Ajustado para ser responsivo */
        margin-bottom: 25px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }

    .rigth {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex: 1;
        /* Para ocupar toda a altura */
    }

    .login {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-left: -85px;
        /* Para ocupar 100% da largura do pai */
        max-width: 400px;
        /* Limitando a largura máxima para evitar problemas em telas muito largas */
        padding: 20px;
        /* Adicionando algum espaçamento interno */
        border-radius: 12px;
    }

    button {
        background-image: linear-gradient(to bottom right, rgb(39, 29, 15), rgb(94, 71, 44));
        color: #fff;
        border-radius: 15px;
        height: 50px;
        width: 100%;
        /* Para ocupar 100% da largura do pai */
        font-size: 1.6em;
        cursor: pointer;
    }

    @media (max-width: 768px) {

        /* Quando a largura da tela for 768 pixels ou menos */
        .box {
            height: auto;
            /* Altura automática para torná-lo responsivo */
        }

        #h1S {
            font-size: 9vw;
            /* Ajustado para ser responsivo em telas pequenas */
            margin-left: 10px;
        }

        #h1L {
            margin-left: 10px;
            font-size: 4vw;
            /* Ajustado para ser responsivo em telas pequenas */

        }

        #h2L {
            font-size: 1.5vw;
            /* Ajustado para ser responsivo em telas pequenas */
            margin-left: 13px;
        }

        #h1lL {
            font-size: 4vw;
            /* Ajustado para ser responsivo em telas pequenas */
        }
    }
</style>

<body>
    <div class="container">
        <div class="box">
            <div class="left"></div>
            <div class="rigth">
                <div class="login">
                    <h1 id="h1lL">Login</h1>
                    <form id="form" method="POST" action="PDO/Autenticar.php">
                        <div class="mb-3">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/gmail.png" width="25px" height="25px" style="margin-right: 5px;">Email:</label>
                            <input type="email" class="form-control" aria-describedby="emailHelp" placeholder="Seu e-mail aqui..." id="email" name="email">
                        </div>
                        <div class="mb-3">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/cadeado.png" width="25px" height="25px" style="margin-right: 5px;">Senha:</label>
                            <input type="password" class="form-control" id="senha" aria-describedby="emailHelp" placeholder="Senha..." name="senha">
                        </div>
                        <div class="mb-3 form-check" style="display: flex;">
                            <input type="checkbox" class="form-check-input" id="ver">
                            <label class="form-check-label" for="exampleCheck1" style="margin-left: 6px;">Ver
                                senha</label>
                            <a href="http://" style="margin-left: 95px;">Esqueceu a senha?</a>
                        </div>
                        <button type="submit" id="logar" name="logar">Entrar</button>
                        <label id="msg2"></label>
                    </form>
                </div>
            </div>
        </div>
    </div>
</body>
<script type="text/javascript">
    
    function verificarCheckbox() {
        var senha = document.getElementById("senha");
        var checkbox = document.getElementById("ver");
        if (checkbox.checked) {
            senha.type = "text";
        } else {
            senha.type = "password";
        }
    }
    // Adiciona um listener ao checkbox para chamar a função quando ele for alterado
    document.getElementById("ver").addEventListener("change", verificarCheckbox);
</script>

</html>