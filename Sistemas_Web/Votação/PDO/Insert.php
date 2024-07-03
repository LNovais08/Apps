<?php 
        require_once("conexao.php");
        $nome =$_POST['nome'];
        $tel =$_POST['tel'];
        $email =$_POST['email'];
        $senha =$_POST['senha'];
        $comp =$_POST['comp'];
        $nivel =$_POST['nivel'];
        $senhaCript = md5($senha);
        $sql = "INSERT INTO competicao.users(Nome,email,celular,competicao,TipoUser,senha,senhaCripto) VALUES('{$nome}','{$email}','{$tel}','{$comp}', '{$nivel}', '{$senha}', '{$senhaCript}')";
        $insert = $pdo -> query($sql);
        echo 'Inserido com Sucesso!!!';
?>