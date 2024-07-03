<!DOCTYPE html>
<?php require_once("PDO/conexao.php") ?>
<?php require_once("PDO/Verificar.php") ?>
<html lang="pt-br">

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
    <style>
        body {
            display: flex;
            margin: 0px;
        }

        header {
            position: absolute;
            top: 0px;
            width: 100%;
            height: 70px;
            background-color: rgb(0, 0, 0);
            display: flex;
            flex-direction: column;
            align-items: start;
            justify-content: center;
        }

        #headerMain {
            width: 100%;
            height: 35px;
            background-color: rgba(41, 40, 40, 0.822);
            color: white;
            font-size: 20px;
        }

        aside {
            position: absolute;
            bottom: 0px;
            left: 0px;
            display: flex;
            flex-direction: column;
            width: 350px;
            height: 849px;
            background-color: rgba(41, 40, 40, 0.822);
        }

        main {
            position: absolute;
            bottom: 0px;
            right: 0px;
            width: 82%;
            height: 849px;
            background-image: url('IMG/bela-foto-de-uma-montanha-de-neve-ao-por-do-sol - Copia.png');
            background-size: cover;
        }

        footer {
            position: absolute;
            bottom: 0px;
            width: 100%;
            height: 20px;
            background-color: rgb(0, 0, 0);
        }

        .btn {
            position: relative;
            left: 45px;
            top: 25px;
            width: 250px;
            height: 50px;
            margin-top: 15px;
            margin-bottom: 5px;
        }


        p {
            color: white;
            font-size: 40px;
            font-style: oblique;
        }

        #btnModal {
            width: 150px;
            margin-bottom: 25px;
        }

        #btn-deletar {
            width: 150px;
            margin-bottom: 25px;
        }

        #btn_CComp {
            width: 150px;
            margin-bottom: 25px;
        }

        #btn-Up {
            width: 150px;
            margin-bottom: 25px;
        }

        #nome {
            font-size: 15px;
            margin-left: 10px;
            margin-top: 15px;
        }

        #nivel {
            font-size: 15px;
            margin-left: 10px;
            margin-top: -30px;
        }
    </style>
    <link rel="shortcut icon" type="" href="IMG/tela-do-laptop.png">
    <title>MDI</title>
</head>
<header>
    <p id="nome">Usuário : <label id="name_user"><?= $_SESSION['Nome'] ?></label>
    <p>
    <p id="nivel">Nível : <label id="nivel"><?= $_SESSION['TipoUser'] ?></label></p>
</header>

<body>
    <aside>
        <button id="btn_CUser" name="btn_CUser" type="button" class="btn btn-dark" onclick="abrirPaginaUs()"><img src="IMG/cadastroUser.png" width="20" height="20"> Cadastrar Usuários</button>
        <!-- Button INSERIR modal -->
        <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#exampleModa2"><img src="IMG/btnCadastroCamp.png"> Cadastrar competições</button>

        <!-- Modal -->
        <div class="modal fade" id="exampleModa2" tabindex="-1" aria-labelledby="exampleModa2Label" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModa2Label">Cadastrando Competições!</h1>
                    </div>
                    <div class="modal-body" id="msg" name="msg" style="display:flex; flex-direction: column; align-items: center; justify-content: center;">
                        <form method="POST" id="form" name="form" class="formulario  d-flex justify-content-center flex-column align-items-center">

                            <div style="display:flex; flex-direction: column; justify-content: center; align-items: center;">
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/nomeCamp.png" width="35" height="35"> Nome :</label>
                                    <input type="text" id="nomeComp" name="nomeComp" placeholder="Nome da competição. . . ." style="margin-left: 15px; width: 300px;">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/calendarioCamp.png" width="35" height="35"> Início :</label>
                                    <input type="date" id="data_inicial" name="data_inicial" style="margin-left: 22px;  width: 120px;">
                                    <label for="" style="margin-top: 5px; margin-left: 8px;">Final :</label>
                                    <input type="date" id="data_final" name="data_final" style="margin-left: 7px; width: 120px;">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/matriculaCamp.png" width="35" height="35">Matricula:</label>
                                    <input type="text" id="matricula" name="matricula" placeholder="xxx.xxx.xxx-xx" style="margin-left: 3px; width: 298px;">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/emailCamp.png" width="35" height="35"> E-mail :</label>
                                    <input type="email" id="emailComp" name="emailComp" placeholder="@email.com" style="margin-left: 15px; width: 300px;">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/CelCamp.png" width="35" height="35"> Celular :</label>
                                    <input type="tel" id="telComp" name="telComp" placeholder="(xx) x xxxx-xxxx" style="margin-left: 10px; width: 300px;">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/CepCamp.png" width="35" height="35"> Cep :</label>
                                    <input type="text" id="cep" name="cep" placeholder="xxxxxxxx" style="margin-left: 32px; width: 300px;">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/esdadoCamp.png" width="35" height="35"> Estado :</label>
                                    <input type="text" id="estado" name="estado" placeholder="Estado. . . . ." style="margin-left: 12px; width: 300px;" disabled="">
                                </div>
                                <div class="linhas" style="display:flex; margin-bottom: 15px;">
                                    <label for=""><img src="IMG/cidadeCamp.png" width="35" height="35"> Cidade :</label>
                                    <input type="text" id="cidade" name="cidade" placeholder="Cidade. . . . ." style="margin-left: 10px; width: 300px;" disabled="">
                                </div>
                                <label class="mensagemIN" id="mensagemIN" name="mensagemIN" style="margin-top:15px; font-size: 25px;"></label>
                            </div>

                        </form>
                    </div>
                    <div class="modal-footer" style="display: flex; align-items: center; justify-content: center;">
                        <button id="btnModal" type="button" class="btn btn-dark" data-bs-dismiss="modal">Close</button>
                        <button type="submit" id="btn_CComp" name="btn_CComp" class="btn btn-dark">Cadastrar</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Button DELETAR modal -->
        <button id="btn_Del" name="btn_Del" type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#exampleModal"><i class="bi bi-trash"></i> Deletar Livro</button>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Deletando Books!</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="msg" name="msg" style="display:flex; flex-direction: column; align-items: center; justify-content: center;">
                        <form method="POST" id="form" name="form" class="formulario  d-flex justify-content-center flex-column align-items-center">

                            <div style="display:flex; flex-direction: column; justify-content: center; align-items: center; height: 80px;">
                                <input type="text" class="form-control fs-2" id="idDelet" name="idDelet" placeholder="Digite o ID do Livro">
                                <label class="mensagem" id="mensagem" name="mensagem" style="margin-top:15px;"></label>
                            </div>

                        </form>
                    </div>
                    <div class="modal-footer" style="display: flex;  align-items: center; justify-content: center;">
                        <button id="btnModal" type="button" class="btn btn-dark" data-bs-dismiss="modal">Close</button>
                        <button type="submit" id="btn-deletar" name="btn-deletar" class="btn btn-dark">Deletar <i class="bi bi-trash3"></i></button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Button UPDATE modal -->
        <button id="btn_Del" name="btn_Del" type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#exampleModa3"><i class="bi bi-arrow-counterclockwise"></i> Atualizar Livros</button>

        <!-- Modal -->
        <div class="modal fade" id="exampleModa3" tabindex="-1" aria-labelledby="exampleModa3Label" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModa3Label">Atualizando Books!</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="msg" name="msg" style="display:flex; flex-direction: column; align-items: center; justify-content: center;height: 430px;">
                        <form method="POST" id="form" name="form" class="formulario  d-flex justify-content-center flex-column align-items-center">

                            <div style="display:flex; flex-direction: column; justify-content: center; align-items: center; height: 120px;">
                                <input type="text" class="form-control fs-2" id="idUp" name="idUp" placeholder="Digite o ID do Livro" style="margin-bottom: 15px;">
                                <input type="text" class="form-control fs-2" id="tituloUp" name="tituloUp" placeholder="Digite o Título do Livro" style="margin-bottom: 15px;">
                                <input type="text" class="form-control fs-2" id="autorUp" name="autorUp" placeholder="Digite o Autor do Livro" style="margin-bottom: 15px;">
                                <input type="text" class="form-control fs-2" id="editoraUp" name="editoraUp" placeholder="Digite a Editora do Livro" style="margin-bottom: 15px;">
                                <input type="text" class="form-control fs-2" id="anoUp" name="anoUp" placeholder="Digite o Ano do Livro">
                                <label class="mensagemUp" id="mensagemUp" name="mensagemUp" style="margin-top:15px;"></label>
                            </div>

                        </form>
                    </div>
                    <div class="modal-footer" style="display: flex;  align-items: center; justify-content: center;">
                        <button id="btnModal" type="button" class="btn btn-dark" data-bs-dismiss="modal">Close</button>
                        <button type="submit" id="btn-Up" name="btn-Up" class="btn btn-dark">Atualizar <i class="bi bi-arrow-counterclockwise"></i></button>
                    </div>
                </div>
            </div>
        </div>

        <button id="btnLogin" type="button" class="btn btn-dark" onclick="abrirPaginaLo()"><i class="bi bi-box-arrow-right"></i> Sair</button>

    </aside>
    <main>
        <header id="headerMain"></header>
    </main>
</body>
<footer></footer>

<script type="text/javascript">
    //mascará para o telefone
    $('#telComp').mask('(00) 0 0000-0000');
    $('#matricula').mask('000.000.000-00');

    //API para CEP
    document.getElementById('cep').addEventListener('blur', function() {
        const cep = this.value.replace(/\D/g, '');

        if (cep.length !== 8) {
            alert('CEP inválido');
            return;
        }

        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert('CEP não encontrado');
                } else {
                    document.getElementById('estado').value = data.uf;
                    document.getElementById('cidade').value = data.localidade;
                }
            })
            .catch(error => console.error('Erro na requisição:', error));
    });
    //Botão Inserir Livros
    $(document).ready(function() {
        $("#btn_CComp").click(function() {
            event.preventDefault();

            //pegando as variáveis pgp na LIB Biblioteca
            <?php require_once("Biblioteca/biblioteca.php"); ?>
            var urlSistema = "<?= $url_sistema ?>";
            var nome = document.getElementById('nomeComp').value;
            var dataI = document.getElementById('data_inicial').value;
            var dataF = document.getElementById('data_final').value;
            var matricula = document.getElementById('matricula').value;
            var email= document.getElementById('emailComp').value;
            var tel = document.getElementById('telComp').value;
            var cep = document.getElementById('cep').value;
            var estado = document.getElementById('estado').value;
            var cidade = document.getElementById('cidade').value;
            var dados = {
                nome: nome,
                dataI: dataI,
                dataF: dataF,
                matricula: matricula,
                email: email,
                tel: tel,
                cep: cep,
                estado: estado,
                cidade: cidade,
            }
            $.ajax({
                url: urlSistema + "PDO/InsertComp.php",
                type: 'POST',
                //Serializando o formulário com suas inputs em vetor

                data: dados,

                success: function(mensagem) {
                    console.log("O caminho do sistema é:" + urlSistema);
                    console.log("Retorno do PHP foi: " + mensagem);
                    document.getElementById('nomeComp').value = "";
                    document.getElementById('data_inicial').value = "";
                    document.getElementById('data_final').value = "";
                    document.getElementById('matricula').value = "";
                    document.getElementById('emailComp').value = "";
                    document.getElementById('telComp').value = "";
                    document.getElementById('cep').value = "";
                    document.getElementById('estado').value = "";
                    document.getElementById('cidade').value = "";
                }

            })
        })
    })
    //Botão DELETAR Livros
    $(document).ready(function() {
        $("#btn-deletar").click(function() {
            event.preventDefault();

            //pegando as variáveis pgp na LIB Biblioteca
            <?php require_once("Biblioteca/biblioteca.php"); ?>
            var urlSistema = "<?= $url_sistema ?>";
            var idLivro = document.getElementById('idDelet').value;
            var dados = {
                id: idLivro,
            }
            $.ajax({
                url: urlSistema + "PDO/DeleteBooks.php",
                type: 'POST',
                //Serializando o formulário com suas inputs em vetor

                data: dados,

                success: function(mensagem) {
                    console.log("O caminho do sistema é:" + urlSistema);
                    console.log("Retorno do PHP foi: " + mensagem);
                    $('#mensagem').text('');
                    $('#mensagem').text(mensagem);
                    document.getElementById('idDelet').value = '';
                }

            })
        })
    })

    //Botão UPDATE Livros
    $(document).ready(function() {
        $("#btn-Up").click(function() {
            event.preventDefault();

            //pegando as variáveis pgp na LIB Biblioteca
            <?php require_once("Biblioteca/biblioteca.php"); ?>
            var urlSistema = "<?= $url_sistema ?>";
            var idLivro = document.getElementById('idUp').value;
            var tituloLivro = document.getElementById('tituloUp').value;
            var autoLivro = document.getElementById('autorUp').value;
            var editoraLivro = document.getElementById('editoraUp').value;
            var anoLivro = document.getElementById('anoUp').value;
            var dados = {
                id: idLivro,
                titulo: tituloLivro,
                autor: autoLivro,
                editora: editoraLivro,
                ano: anoLivro,
            }
            $.ajax({
                url: urlSistema + "PDO/UpdateBooks.php",
                type: 'POST',
                //Serializando o formulário com suas inputs em vetor

                data: dados,

                success: function(mensagem) {
                    console.log("O caminho do sistema é:" + urlSistema);
                    console.log("Retorno do PHP foi: " + mensagem);
                    $('#mensagemUp').text('');
                    $('#mensagemUp').text(mensagem);
                    document.getElementById('idUp').value = '';
                    document.getElementById('tituloUp').value = '';
                    document.getElementById('autorUp').value = '';
                    document.getElementById('anoUp').value = '';
                    document.getElementById('editoraUp').value = '';
                }

            })
        })
    })

    //Botão SAIR 
    function abrirPaginaLo() {
        // Substitua 'url_da_pagina' pelo URL da página que deseja abrir
        window.location.href = 'PDO/logout.php';
    }
    //Botão User
    function abrirPaginaUs() {
        var nivelUser = <?= '"' . $_SESSION['TipoUser'] . '"' ?>;
        if (nivelUser == "ADM") {
            window.location.href = 'Cadastro.php';
        } else {
            Swal.fire({
                title: "Hmm, algo deu errado.",
                html: "Você NÃO tem acesso a essas informações.",
                icon: "error"
            })
        }
    }
</script>

</html>