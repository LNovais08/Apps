<?php
require_once("conexao.php");
$email = $_POST['email'];
$senha = $_POST['senha'];

$sql = "SELECT * FROM laís.sistemaweb_usuarios WHERE email = '$email' AND senha = '$senha'";
$result = $pdo->query($sql);

if($result->rowCount() > 0){
    echo"Encontrados com sucesso!";
} else {
    echo"NÃO foram encontrados!";
}
?>