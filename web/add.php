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
	$record2 = $databaseConnection->prepare("SELECT tick from ".$tablename."");
        $record2->execute();
	$ilist = array();
        while($data2 = $record2->fetch(PDO::FETCH_ASSOC)){
		$ilist[] =  $data2['tick'];
	}
	foreach($_POST['ticks'] as $tick){
		if (!in_array($tick,$ilist)){
			$record1 = $databaseConnection->prepare("INSERT INTO ".$tablename." (tick, share, status, frequency) VALUES ( :tick, 0, 0, \"auto\")");
			$record1->bindParam(':tick', $tick, PDO::PARAM_STR);
		       	$record1->execute();
		}
        }
	$page ="https://jsong-investment.xyz/viewprofile.php?val=".$name;
	header( "Location: $page");
}else {
	echo ("<SCRIPT LANGUAGE='JavaScript'>
                        window.alert('Unknown Table Name')
                        </SCRIPT>");
}
?>
