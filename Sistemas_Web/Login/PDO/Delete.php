<?php 

        require_once("conexao.php");
        $id =$_POST['id'];
        $sql = "DELETE FROM ibituruna.livros WHERE id = :id";
        $result = $pdo->prepare($sql);
        $result->bindValue(':id',$id);
        $count = $result->execute();
        echo 'Deletado com sucesso';

?>