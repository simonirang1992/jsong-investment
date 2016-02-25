<!DOCTYPE html>
<?php
include_once 'db.php';
session_start();
if(!isset($_SESSION['member']))
{
 header("Location: login.php");
}
$username = $_SESSION['member'];
$type = $_SESSION['type'];
$pname = $_POST['pname'];
$fund = $_POST['funds'];
$password = $_POST['apassword'];
if (empty($pname) || empty($fund) || empty($password) || !is_numeric($fund)) {
	echo ("<SCRIPT LANGUAGE='JavaScript'>
			window.alert('One of your field is invalid!')
        		window.location.href='https://jsong-investment.xyz/createp.php'
        		</SCRIPT>");
	exit;
}else {
$t="1111";
$a="admin";
$pname = stripslashes($pname);
$fund = stripslashes($fund);
$password = stripslashes($password);
$tablename="profile_".$username."_".$pname;
if ((strcmp($password, $t) == 0) && (strcmp($type, $a) == 0)){
        $record = $databaseConnection->prepare('INSERT INTO userprofile (tablename, id, fund, init) VALUES (:pname, (SELECT id from account WHERE username = :username), :fund, :init)');
       	$record->bindParam(':username', $username, PDO::PARAM_STR);
        $record->bindParam(':pname', $pname, PDO::PARAM_STR);
        $record->bindParam(':fund', $fund, PDO::PARAM_STR);
	$record->bindParam(':init', $fund, PDO::PARAM_STR);
	$record->execute();

	$record = $databaseConnection->prepare('CREATE TABLE '.$tablename.' (id INT(5) AUTO_INCREMENT, tick VARCHAR(10) NOT NULL, share VARCHAR(10) NOT NULL, monitor VARCHAR(5) NOT NULL, status VARCHAR(10) NOT NULL, frequency VARCHAR(10) NOT NULL, PRIMARY KEY(id))');
        $record->execute();
	echo ("<SCRIPT LANGUAGE='JavaScript'>
                        window.alert('Created Profile!')
                        window.location.href='https://jsong-investment.xyz/createp.php'
                        </SCRIPT>");

} else {
	 echo ("<SCRIPT LANGUAGE='JavaScript'>
                        window.alert('You are not allow to perform this operation!')
                        window.location.href='https://jsong-investment.xyz/createp.php'
                        </SCRIPT>");
}

}

?>

