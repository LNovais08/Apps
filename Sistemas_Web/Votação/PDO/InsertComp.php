<?php 
        require_once("conexao.php");
        $nome =$_POST['nome'];
        $dataI =$_POST['dataI'];
        $dataF =$_POST['dataF'];
        $matricula =$_POST['matricula'];
        $email =$_POST['email'];
        $tel =$_POST['tel'];
        $cep =$_POST['cep'];
        $estado =$_POST['estado'];
        $cidade =$_POST['cidade'];
        $sql = "INSERT INTO competicao.competicao(NomeCompeticao,InicioCompeticao,FimCompeticao,MatriculaResponsavel,emailContato,celularContato,CEPSenac,CidadeCompeticao,UFCompeticao) VALUES('{$nome}','{$dataI}','{$dataF}','{$matricula}', '{$email}', '{$tel}', '{$cep}'), '{$estado}', '{$cidade}')";
        $insert = $pdo->query($sql);
        if($insert){
            echo 'Inserido com Sucesso!!!';
        } else {
            echo 'ERROR . . .. .';
        }
        
?>