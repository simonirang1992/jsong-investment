<?php

$host='localhost';
$dbname='user';
$username='user';
$password='password';
//PDO Database Connection
try {
	$dsn = "mysql:host=$host;dbname=$dbname";
	$databaseConnection = new PDO($dsn, $username, $password);

	$databaseConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
	echo 'ERROR: ' . $e->getMessage();
}
?>
