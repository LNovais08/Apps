<?php
//Pega a data atuaL:
setlocale(LC_TIME, 'pt-BR', 'pt_BR.utf-8', 'pt_BR.utf-8', 'portuguese');
date_default_timezone_set('America/Sao_Paulo');
$data_hoje = utf8_encode(strftime('%A, %d de %B de %Y', strtotime('today')));
$hora_hoje = date('H:i:s');
//echo $data_hoje;

$nome_sistema = "SistemaWeb";
$email_sistema = "lais.novais@gmail.com";
$telefone_sistema = "(35)0000-0000";
$url_sistema = 'http://localhost/Tela_Login_Votação/';

?>