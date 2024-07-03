<?php
require_once("conexao.php");
$id2 = $_POST['id'];
$nome2 = $_POST['nome'];
$autor2 = $_POST['autor'];
$editora2 = $_POST['editora'];
$ano2 = $_POST['ano'];
$sql = "UPDATE ibituruna.livros SET titulo = '$nome2',autor= '$autor2',editora='$editora2',ano = '$ano2' WHERE id= $id2";
echo $sql;
$result = $pdo->query($sql);

 //echo"Atualizada com sucesso!";
?>