<?php
require_once("conexao.php");
$id = $_POST['id'];
$titulo = $_POST['titulo'];
$autor = $_POST['autor'];
$editora = $_POST['editora'];
$ano = $_POST['ano'];

$queryinser=$pdo->query("UPDATE livros SET titulo='$titulo', autor='$autor', editora='$editora', ano='$ano' WHERE id='$id'");
echo "Foi Atualizado....";

?>