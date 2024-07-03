<?php
require_once("../Biblioteca/biblioteca.php");
require_once("../PDO/conexao.php");
session_start();
session_destroy();
header('Location:' . $url_sistema . 'index.php');
?>