<?php
require_once("conexao.php");
require_once("../Biblioteca/biblioteca.php");
$id =$_POST['id'];
$sql = "DELETE FROM ibituruna.livros WHERE id = :id";
$result = $pdo->prepare($sql);
$result->bindValue(':id',$id);
$count = $result->execute();
$resposta = "Registro Deletado em: <h3 style = 'color: white;'>" . $data_hoje . ' - ' . $hora_hoje . "</h3>";
echo "Deletado com Sucesso";
?>

