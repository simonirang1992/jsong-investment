<!DOCTYPE html>
<?php
session_start();
include_once 'db_data.php';
if(!isset($_SESSION['member']))
{
 header("Location: login.php");
}
$username = $_SESSION['member'];
$type = $_SESSION['type'];
$tick = $_POST['mbutton'];

// Only Admin should be able to use it
if (strcmp($type,"admin") == 0){
	$record1 = $databaseConnection1->prepare('SELECT manual, enabledp from ticklist WHERE tick = :tick');
	$record1->bindParam(':tick', $tick, PDO::PARAM_STR);
	$record1->execute();
	$result = $record1->fetch(PDO::FETCH_ASSOC);
	if ($result == false){
		echo ("<SCRIPT LANGUAGE='JavaScript'>
			window.alert('Tick Does not Exists!')
        		window.location.href='https://jsong-investment.xyz/info.php'
        		</SCRIPT>");
	} else {
		if (strcmp($result['manual'], "1") == 0){
			$status = "0";
			$ts = "0";
		} else {
			$status = "1";
			if (empty($result['enabledp'])){
				$ts = "1";
			} else {
				$ts = "0";
			}
		}

		$record1 = $databaseConnection1->prepare('UPDATE ticklist set enabled = :ts, manual = :status WHERE tick = :tick');
		$record1->bindParam(':ts', $ts, PDO::PARAM_STR);
		$record1->bindParam(':status', $status, PDO::PARAM_STR);
		$record1->bindParam(':tick', $tick, PDO::PARAM_STR);
        	$record1->execute();
		echo ("<SCRIPT LANGUAGE='JavaScript'>
        		window.alert('Succesfully Updated')
        		window.location.href='https://jsong-investment.xyz/info.php'
       		 	</SCRIPT>");
		}
} else {
	echo ("<SCRIPT LANGUAGE='JavaScript'>
        window.alert('You are not permitted to do this operation')
        window.location.href='https://jsong-investment.xyz/info.php'
        </SCRIPT>");
}
?>

