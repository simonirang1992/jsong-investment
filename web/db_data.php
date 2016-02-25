<?php
$host1='localhost';
$dbname1='jsong';
$username1='user';
$password1='password';
//PDO Database Connection
try {
	$dsn1 = "mysql:host=$host1;dbname=$dbname1";
	$databaseConnection1 = new PDO($dsn1, $username1, $password1);

	$databaseConnection1->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
	echo 'ERROR: ' . $e->getMessage();
}
?>
