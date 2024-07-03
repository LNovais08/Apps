<?php
try{

    //Criando variaveis para a conexão
    $host = "172.16.54.174:3310";
    $username = 'root';
    $password = '';
    $DB_PORT = '3310';
    $BASE = 'competicao';
    $pdo = new PDO("mysql:host=$host;dbname=$BASE;charset=utf8", $username, $password);
    //echo 'CONECTADO';

} catch (Exception $e){
    echo 'ERRO<br>';
    echo $e;
}