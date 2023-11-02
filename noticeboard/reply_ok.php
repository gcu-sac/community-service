<?php
    include "../db_info.php";
?>
<?php
  error_reporting(E_ALL);
  ini_set("display_errors", 1);
?>
<?php
    session_save_path('../../session');
    session_start();
    $bno = $_GET['idx'];
    $user = $_SESSION['name'];
    $pw = $_SESSION['password'];
    $content = $_POST['content'];
    $date = date("Y-m-d H:i:s",time());
    
    if($bno && $user && $pw && $content) {
        $sql = "insert into reply(con_num,id,pw,content,date) values('".$bno."','".$user."','".$pw."','".$content."','".$date."')";
        echo $sql;
        sq($sql);
        echo "<script>
                alert('댓글이 작성되었습니다.'); 
                location.href='read.php?idx=$bno';
              </script>";
     }else {
        echo "<script>
                alert('댓글 작성에 실패했습니다.'); 
                location.href='read.php?idx=$bno';
              </script>";
    }
	
?>