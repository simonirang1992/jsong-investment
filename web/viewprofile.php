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
$val = $_GET['val'];
$val = stripslashes($val);
?>
<html>
<head>
<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
<title> View Profile </title>
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
              <li><a href="profile.php">Profile</a></li>
	      <li><a href="info.php">Company Profile</a></li>
	      <li><a href="createp.php"> Create Profile</a></li>
<?php
	      echo "<li class=\"active\"><a href=\"viewprofile.php?val=".$val."\"> View Profile - $val </a></li>";
	      echo "<li><a href=\"modify.php?name=".$val."&func=add\"><p> Add Companies </p></a></li>";
	      echo "<li><a href=\"modify.php?name=".$val."&func=remove\"><p> Remove Companies </p></a></li>";
?>
	      <li><a href="logout.php">Logout</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>


<table id="corplist" class="tablesorter table table-hover table-striped" border="1" align="center">
<tr>
<th style="text-align:center"> Tick </th>
<th style="text-align:center"> Shares </th>
<th style="text-align:center"> Monitor </th>
<th style="text-align:center"> Status </th>
<th style="text-align:center"> Frequency </th>
<th style="text-align:center"> Market Price </th>
<th style="text-align:center"> Current Value </th>
</tr>
<?php
$tname = "profile_".$username."_".$val;
$record = $databaseConnection->prepare('SELECT * FROM '.$tname);
$record->execute();
while($data = $record->fetch(PDO::FETCH_ASSOC)){
	echo "<tr>";
	echo "<td align=\"center\"><a href=cprofile.php?name=".$data['tick'].">".$data['tick']."</a></td>";
	$ishare = intval($data['share']); // might have to fix this later
	echo "<td align=\"center\">".$data['share']."</td>";
	if (($data['monitor'] == null) || ($data['monitor'] == 0)){
		echo "<td align=\"center\"><img src=\"img/error.png\"></td>";
	}
	else {
		echo "<td align=\"center\"><img src=\"img/check.png\"></td>";
	}

	if ($data['status'] == 0) {
		echo "<td align=\"center\"><img src=\"img/check.png\"></td>";
	} else {
		echo "<td align=\"center\"><img src=\"img/error.png\"></td>";
	}
	echo "<td align=\"center\">".$data['frequency']."</td>";
	$record1 = $databaseConnection1->prepare('SELECT ask FROM yql_real WHERE tick = "'.$data['tick'].'"');
	$record1->execute();
	while($data1 = $record1->fetch(PDO::FETCH_ASSOC)){
		echo "<td align=\"center\">".$data1['ask']."</td>";
		$marketval = intval($data1['ask']) * $ishare;
		echo "<td align=\"center\">".$marketval."</td>";
	}
	echo "</tr>";
}
?>
</table>
</body>
</html>

