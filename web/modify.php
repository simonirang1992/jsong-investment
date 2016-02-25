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
$val = $_GET['name'];
$func = $_GET['func'];
$val = stripslashes($val);
$func = stripslashes($func);
?>
<html>
<head>
<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

<title> View Profile </title>


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
	      echo "<li><a href=\"viewprofile.php?val=".$val."\"> View Profile - $val </a></li>";
	if (strcmp($func,"add") ==0){
		echo "<li class=\"active\"><a href=\"modify.php?name=".$val."&func=add\"><p> Add Companies </p></a></li>";
		echo "<li><a href=\"modify.php?name=".$val."&func=remove\"><p> Remove Companies </p></a></li>";
	} elseif (strcmp($func, "remove") == 0){
		echo "<li><a href=\"modify.php?name=".$val."&func=add\"><p> Add Companies </p></a></li>";
		echo "<li class=\"active\"><a href=\"modify.php?name=".$val."&func=remove\"><p> Remove Companies </p></a></li>";
	}
?>
	      <li><a href="logout.php">Logout</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>

<?php 
if (strcmp($func,"add") == 0){
	$tname= "profile_".$username."_".$val;
	
?>
	<form action="add.php" method="POST">
<?php
	echo "<input type=\"hidden\" name=\"table\" value=\"$val\">";

?>
	<input type="submit" value="Submit">
	<table id="corplist" class="tablesorter" border="1" align="center">
        <thead>
        <tr>
                <th> Tick </th>
                <th> Sector </th>
                <th> Industry </th>
                <th> Market Value </th>
                <th> Beta </th>
                <th> Enable </th>
        </tr>
        </thead>
        <tbody>

<?php
	$record1 = $databaseConnection1->prepare('SELECT ticklist.enabledp, ticklist.tick, ticklist.sector, ticklist.industry, yql_real.smc, yql_day.beta, ticklist.enabledp FROM ticklist, yql_real, yql_day WHERE ticklist.tick = yql_real.tick AND ticklist.tick = yql_day.tick');
	$record1->execute();
	while($data1 = $record1->fetch(PDO::FETCH_ASSOC)){
		$enabledfunc = explode(",", $tname);
		for ($i = 0; $i < count($enabledfunc); $i++){
			if ($enabledfunc[$i] == $tname){
				echo "<tr>";
				echo "<td align=\"center\"><a href=cprofile.php?name=".$data1['tick'].">".$data1['tick']."</a></td>";
				echo "<td align=\"center\">".$data1['sector']."</td>";
				echo "<td align=\"center\">".$data1['industry']."</td>";
				echo "<td align=\"center\">".$data1['smc']."</td>";
				echo "<td align=\"center\">".$data1['beta']."</td>";
				echo "<td align=\"center\"><input type=\"checkbox\" name=\"ticks[]\" value=\"".$data1['tick']."\"></td>";
				echo "</tr>";
			}
		}
	}
?>
</tbody>
</table>
</form>
<?php
} elseif (strcmp($func, "remove") == 0){
	$tname = "profile_".$username."_".$val;
	$record = $databaseConnection->prepare('SELECT * FROM '.$tname);
	$record->execute();
	echo $val;?>
	<form action="remove.php" method="POST">
	<table border = 1>
	<tr>
	<th> Tick </th>
	<th> Share </th>
	<th> Monitor </th>
	<th> Status </th>
	<th> Frequency </th>
	<th> Delete </th>
	</tr>
	<?php
	while($data = $record->fetch(PDO::FETCH_ASSOC)){
        	echo "<tr>";
       		echo "<td align=\"center\">".$data['tick']."</td>";
       		echo "<td align=\"center\">".$data['share']."</td>";
       		echo "<td align=\"center\">".$data['monitor']."</td>";
        	echo "<td align=\"center\">".$data['status']."</td>";
        	echo "<td align=\"center\">".$data['frequency']."</td>";
		echo "<td align=\"center\"><input type=\"checkbox\" name=\"ticks[]\" value=\"".$data['tick']."\"></td>";
        	echo "</tr>";
	}
	?>
	</table>
	<br>
	<?php
	echo "<input type=\"hidden\" name=\"table\" value=\"$val\">";
	?>
	<input type="submit" value="Submit">
	</form>
<?php

} else {
	echo ("<SCRIPT LANGUAGE='JavaScript'>
                        window.alert('Invalid Operation!!')
                        window.location.href='https://jsong-investment.xyz/profile.php'
                        </SCRIPT>");

}

?>





<br>
<script src="//code.jquery.com/jquery-2.1.4.min.js"></script> 
<script src="//rawgit.com/christianbach/tablesorter/master/jquery.tablesorter.min.js"></script> 
<script>
        $("#corplist").tablesorter();
</script>
</body>
</html>

