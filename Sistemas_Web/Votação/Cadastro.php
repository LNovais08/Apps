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
    <!-- Mascará para formatar a input telefone -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <?php require_once("PDO/conexao.php") ?>
    <link rel="shortcut icon" type="" href="IMG/cadastro.png">
    <title>Cadastro</title>
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
        height: 700px;
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
        background-image: url('IMG/cada.png');
        background-repeat: no-repeat;
        background-size: cover;
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
        flex: 1.2;
        /* Para ocupar toda a altura */
        position: relative;
        /* Adicionado para posicionar elementos filhos absolutamente */
    }

    .caixaFont {
        display: flex;
        flex-direction: column;
        align-items: start;
        position: absolute;
        top: 50%;
        /* Ajustado para o centro vertical */
        transform: translateY(-50%);
        /* Ajustado para o centro vertical */
        width: 100%;
        text-align: center;
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
        font-size: 3.3vw;
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
        /* Para ocupar 100% da largura do pai */
        max-width: 400px;
        /* Limitando a largura máxima para evitar problemas em telas muito largas */
        padding: 20px;
        /* Adicionando algum espaçamento interno */
        border-radius: 12px;
    }

    button {
        background: #403a26e7;
        color: #fff;
        border-radius: 15px;
        height: 50px;
        width: 100%;
        /* Para ocupar 100% da largura do pai */
        font-size: 1.6em;
        cursor: pointer;
    }

    select {
        margin-left: 10px;
        height: 25px;
        width: 250px;
        border-radius: 7px;
        border: none;
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
                    <h1 id="h1lL">Cadastro</h1>
                    <form id="form" method="POST" style="width: 320px;">
                        <div class="mb-2">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/eu-iria.png" width="25px" height="25px" style="margin-right: 5px;">Nome:</label>
                            <input type="text" class="form-control" aria-describedby="emailHelp" placeholder="Seu nome aqui..." id="nome" name="nome">
                        </div>
                        <div class="mb-2">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/telefone-velho.png" width="25px" height="25px" style="margin-right: 5px;">Celular:</label>
                            <input type="tel" class="form-control" aria-describedby="emailHelp" placeholder="(xx) x xxxx-xxxx" id="tel" name="tel">
                        </div>
                        <div class="mb-2">

                        </div>
                        <div class="mb-2">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/gmail.png" width="25px" height="25px" style="margin-right: 5px;">Email:</label>
                            <input type="email" class="form-control" aria-describedby="emailHelp" placeholder="Seu e-mail aqui..." id="email" name="email">
                        </div>
                        <div class="mb-3">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/cadeado.png" width="25px" height="25px" style="margin-right: 5px;">Senha:</label>
                            <input type="password" class="form-control" id="senha" aria-describedby="emailHelp" placeholder="Senha" name="senha">
                        </div>
                        <div class="mb-3" style="display: flex;">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex; margin-top: 5px;"><img src="IMG/CampUser.png" width="25px" height="25px" style="margin-right: 5px;">Competição:</label>
                            <select name="comp" id="comp" style="margin-left: 6px; height: 30px; margin-left: 15px;">
                                <?php
                                require_once('./PDO/conexao.php');
                                $sql = "SELECT NomeCompeticao FROM competicao.competicao";
                                $result = $pdo->query($sql);
                                $res = $result->fetchAll(PDO::FETCH_ASSOC);
                                $count = count($res);
                                for ($i = 0; $i <= $count - 1; $i++) {
                                    echo '<option value= "' . $res[$i]['NomeCompeticao'] . '">' . $res[$i]['NomeCompeticao'] . '</option>';
                                }
                                ?>
                            </select>
                        </div>
                        <div class="mb-1" style="display: flex;">
                            <label for="exampleInputEmail1" class="form-label" style="display: flex;"><img src="IMG/nivelUse.png" width="25px" height="25px" style="margin-right: 5px;">Nivel:</label>
                            <select name="nivel" id="nivel">
                                <option value="ADM">adm</option>
                                <option value="USER">user</option>
                            </select>
                        </div>
                        <div class="mb-3 form-check" style="display: flex;">
                            <input type="checkbox" class="form-check-input" id="ver">
                            <label class="form-check-label" for="exampleCheck1" style="margin-left: 6px;">Ver senha</label>
                        </div>
                        <button type="submit" id="cadastrar" name="cadastrar">Cadastrar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

</body>
<script type="text/javascript">
    //mascará para o telefone
    $('#tel').mask('(00) 0 0000-0000');
    $('#cep').mask('00000-000');

    $(document).ready(function() {
        $("#cadastrar").click(function() {
            event.preventDefault();

            //pegando as variáveis pgp na LIB Biblioteca
            <?php require_once("Biblioteca/biblioteca.php"); ?>
            var urlSistema = "<?= $url_sistema ?>";
            if (document.getElementById('nome').value == "" || document.getElementById('tel').value == "" || document.getElementById('email').value == "" || document.getElementById('senha').value == "") {
                Swal.fire({
                    title: "Hmm, algo deu errado.<br>Seu Cadastro NÃO foi efetuado.",
                    html: "Confira se você preencheu todos os campos!<br>Tente novamente!",
                    icon: "error"
                })
            } else {
                var nome1 = document.getElementById('nome').value;
                var telefone1 = document.getElementById('tel').value;
                var email1 = document.getElementById('email').value;
                var senha1 = document.getElementById('senha').value;
                var comp = document.getElementById('comp').value;
                var nivel = document.getElementById('nivel').value;

                var dados = {
                    nome: nome1,
                    tel: telefone1,
                    email: email1,
                    senha: senha1,
                    comp: comp,
                    nivel: nivel,
                }
                $.ajax({
                    url: urlSistema + "PDO/Insert.php",
                    type: 'POST',
                    //Serializando o formulário com suas inputs em vetor

                    data: dados,

                    success: function(mensagem) {
                        console.log("O caminho do sistema é:" + urlSistema);
                        console.log("Retorno do PHP foi: " + mensagem);
                        if (mensagem.trim() == "Inserido com Sucesso!!!") {
                            Swal.fire({
                                title: "Cadastro efetuado com sucesso!",
                                html: "Bem-vindo!<br>Agora  pode ralizar seu login!",
                                icon: "seccess",
                                showCancelButton: true,
                                confirmButtonText: 'Voltar ao MDI',
                                cancelButtonText: 'Cancelar'
                            }).then((result) => {
                                // Se o usuário clicou em "Sim, fazer login", redireciona para a página de login.html
                                if (result.isConfirmed) {
                                    window.location.href = 'Logado.php';
                                }
                            });
                        } else {
                            Swal.fire({
                                title: "Hmm, algo deu errado.<br>Seu Cadastro NÃO foi efetuado.",
                                html: "Confira se você preencheu todos os campos!<br>Tente novamente!",
                                icon: "error"
                            })
                        }
                    }

                })
            }


        })
    })


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