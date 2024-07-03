<?php 
        require_once("conexao.php");
        $nome =$_POST['nome'];
        $tel =$_POST['tel'];
        $sexo =$_POST['sexo'];
        $email =$_POST['email'];
        $senha =$_POST['senha'];
        $sql = "INSERT INTO usuarios(nome,telefone,sexo,email,senha) VALUES('{$nome}','{$tel}','{$sexo}','{$email}', '{$senha}')";
        $insert = $pdo -> query($sql);
        echo 'Inserido com Sucesso!!!';
?>