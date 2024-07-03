<?php
session_start();
require_once("../Biblioteca/biblioteca.php");
require_once("../PDO/conexao.php");


if(isset($_POST['email']) && !empty($_POST['email'])){
    $email =$_POST['email'];
    $senha =$_POST['senha'];
} else {
    header('Location:' . $url_sistema . 'Logado.php');
    exit();
}
$trim1 = trim($email);

$sql = "SELECT * FROM competicao.users WHERE email = :email";
$result = $pdo->prepare($sql);
$result->bindValue(':email',"$trim1");
$res = $result->execute();
$res = $result->fetchAll(PDO::FETCH_ASSOC);
$nome = $res[0]['Nome'];
$nivel = $res[0]['TipoUser'];
$pass = $res[0]['senhaCripto'];
$senhaC = md5($senha);

if($senhaC == $pass){
    $_SESSION['email']= $email;
    $_SESSION['Nome'] = $nome;
    $_SESSION['TipoUser'] = $nivel;
    header('Location:' . $url_sistema . 'Logado.php');
} else {
    header('Location:' . $url_sistema . 'index.php');
    session_destroy();
    echo "Swal.fire('Usuário não encontrado')";
    exit;
}
?>