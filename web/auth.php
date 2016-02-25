<?php
include_once 'db.php';
if (isset($_SESSION['member'])){
	header("Location: profile.php");
	exit;
}


if (isset($_POST['submit'])){
	$username = $_POST['username'];
	$password = $_POST['password'];

	if (empty($username) || empty($password)) {
                //$error = "Username or Password is invalid";
                $errval = 1;
        }


	$username = stripslashes($username);
	$password = stripslashes($password);

	$record = $databaseConnection->prepare('SELECT username, password, type FROM account WHERE username = :username AND password = :password');
	$record->bindParam(':username', $username, PDO::PARAM_STR);
	$record->bindParam(':password', $password, PDO::PARAM_STR);
	$record->execute();
	//$result = $record->fetchColumn();
	$result = $record->fetch(PDO::FETCH_ASSOC);

	if ($result == false){
		//$error = 'Incorrect Username or Passsword';
		$errval = 1;
	} else {
		$_SESSION['member'] = $result['username'];
		$_SESSION['type'] = $result['type'];
		header('location:profile.php');
 		exit;
	}

}
?>
