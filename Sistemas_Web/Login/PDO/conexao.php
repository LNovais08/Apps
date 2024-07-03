<?php
try{

    //Criando variaveis para a conexão
    $host = "127.0.0.1:3306";
    $username = 'root';
    $password = '';
    $DB_PORT = '3306';
    $BASE = 'sistemaweb_login';
    $pdo = new PDO("mysql:host=$host;dbname=$BASE;charset=utf8", $username, $password);
    //echo 'CONECTADO';

} catch (Exception $e){
    echo 'ERRO<br>';
    echo $e;
}