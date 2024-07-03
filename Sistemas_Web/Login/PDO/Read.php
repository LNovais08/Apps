<?php 
        require_once("conexao.php");
        $queryLivros = $pdo->query($sql);
        $res = $queryLivros->fetchAll(PDO::FETCH_ASSOC);
        return $res;
?>