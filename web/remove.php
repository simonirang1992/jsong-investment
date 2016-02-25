<!DOCTYPE html>
<?php
session_start();
if(!isset($_SESSION['member']))
{
 header("Location: login.php");
}

include_once 'db.php';
include_once 'db_data.php';

$username = $_SESSION['member'];
$type = $_SESSION['type'];
if(!empty($_POST['table'])){
	$name = $_POST['table'];
	$tablename = "profile_".$username."_".$name;
	foreach($_POST['ticks'] as $tick) {
		$record2 = $databaseConnection->prepare('DELETE FROM '.$tablename.' WHERE tick = :tick');
		$record2->bindParam(':tick', $tick, PDO::PARAM_STR);
	       	$record2->execute();

	}
	echo ("<SCRIPT LANGUAGE='JavaScript'>
                        window.alert('Deleted Company')
                        </SCRIPT>");
	header("Location: viewprofile.php?val=".$name);
}else {
	echo ("<SCRIPT LANGUAGE='JavaScript'>
                        window.alert('Unknown Table Name')
                        </SCRIPT>");

}
?>
