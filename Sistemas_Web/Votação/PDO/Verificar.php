<?php
require_once('./Biblioteca/biblioteca.php');
session_start();
if(!isset($_SESSION['email'])){

    header('location:' . $url_sistema);
    exit();
}
?>