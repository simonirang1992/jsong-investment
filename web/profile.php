<!DOCTYPE html>
<?php
session_start();
if(!isset($_SESSION['member']))
{
 header("Location: login.php");
}

include_once 'db.php';

$username = $_SESSION['member'];
?>
<html>
<head>
<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
<title> User Profile </title>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

</head>


<body>
      <nav class="navbar navbar-default">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">JSONG-INVESTMENT  </a>
          </div>
          <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li><a href="index.php">Home</a></li>
              <li class="active"><a href="profile.php">Profile</a></li>
              <li><a href="info.php">Company Profile</a></li>
              <li><a href="logout.php">Logout</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>


<?php

$record = $databaseConnection->prepare('SELECT tablename, fund, init from userprofile WHERE id = (SELECT id FROM account WHERE username = :username)');
$record->bindParam(':username', $username, PDO::PARAM_STR);
$record->execute();
?>

<table id="corplist" class="tablesorter table table-hover table-striped" border="1" align="center">
<tr>
<th style="text-align:center"> Profile Name </th>
<th style="text-align:center"> Funds </th>
</tr>

<?php
while($data = $record->fetch(PDO::FETCH_ASSOC)){
	$tname = str_replace("profile_".$username."_", "", $data['tablename']);
	echo "<tr>";
	echo "<td align=\"center\">";
	echo "<a href=viewprofile.php?val=".$tname.">".$tname."</a>";
	echo "</td>";
	echo "<td align=\"center\">";
	echo $data['fund'];
	echo "</td>";
	echo "</tr>";
}
?>
</table>
</body>
</html>

