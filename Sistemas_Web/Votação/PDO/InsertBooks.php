<?php
require_once("conexao.php");
$titulo =$_POST['titulo'];
$autor =$_POST['autor'];
$editora =$_POST['editora'];
$ano =$_POST['ano'];

$queryinser=$pdo->query("INSERT INTO livros(titulo,autor,editora,ano) VALUES('{$titulo}','{$autor}','{$editora}','{$ano}')");
echo "Livro inserido com sucesso....";

?>


