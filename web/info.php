<!DOCTYPE html>
<?php
session_start();
if(!isset($_SESSION['member']))
{
 header("Location: login.php");
}
$dsn = null;
include_once 'db_data.php';
?>
<html>
<head>
<style type="text/css">
</style>

<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
<title> Company Profile Status</title>
<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
<style>

.table tbody tr:hover td, .table tbody tr:hover th {
    background-color: #ffbf80;
    page-break-inside: avoid;
    overflow-x: visible;
    align=: center;
}
</style>

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
	      <li class="active"><a href="info.php">Company Profile</a></li>
	      <li><a href="createp.php"> Create Profile</a></li>
              <li><a href="logout.php">Logout</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>

<div class="row">
	
</div>

<div class="row">
<div class="col-sm-1"></div>
<div class="col-sm-10">
<form action="enable.php" method="POST">
<div class="table-responsive">
<table id="corplist" class="tablesorter table table-hover table-striped" border="1" align="center">
	<thead align="center">
	<tr>
		<th style="text-align:center"> Tick </th>
		<th style="text-align:center"> Enabled </th>
		<th style="text-align:center"> Status </th>
		<th style="text-align:center"> Manual </th>
		<th style="text-align:center"> Sector </th>
		<th style="text-align:center"> Industry </th>
		<th style="text-align:center"> Market Value </th>
		<th style="text-align:center"> Beta </th>
	<!--	<th> Error Functions </th> -->
	</tr>
	</thead>
	<tbody>
<?php
	$record1 = $databaseConnection1->prepare('SELECT ticklist.tick, ticklist.enabled, ticklist.status, ticklist.manual, ticklist.sector, ticklist.industry, yql_real.smc, yql_day.beta, ticklist.errorfnc FROM ticklist, yql_real, yql_day WHERE ticklist.tick = yql_real.tick AND ticklist.tick = yql_day.tick');
	$record1->execute();
	while($data1 = $record1->fetch(PDO::FETCH_ASSOC)){
		echo "<tr>";
		echo "<td align=\"center\"><a href=cprofile.php?name=".$data1['tick'].">".$data1['tick']."</a></td>";
		if ($data1['enabled'] == 0){
			echo "<td align=\"center\"><img src=\"img/check.png\"></td>";
			//echo "<td align=\"center\"><input type=\"image\" src=\"img/check.png\" name=\"mbutton\" value=\"".$data1['tick']."\"></td>";
		} else {
			//echo "<td align=\"center\"><input type=\"image\" src=\"img/error.png\" name=\"mbutton\" value=\"".$data1['tick']."\"></td>";

			echo "<td align=\"center\"><img src=\"img/error.png\"></td>";
		}

		if ($data1['status'] == 0) {
			echo "<td align=\"center\"><img src=\"img/check.png\"></td>";
		} else {
			echo "<td align=\"center\"><img src=\"img/error.png\"></td>";
		}

		if ($data1['manual'] == 0) {
			echo "<td align=\"center\"><input type=\"image\" src=\"img/on.png\" name=\"mbutton\" value=\"".$data1['tick']."\"></td>";
		} else {
			echo "<td align=\"center\"><input type=\"image\" src=\"img/off.png\" name=\"mbutton\" value=\"".$data1['tick']."\"></td>";
		}

		echo "<td align=\"center\">".$data1['sector']."</td>";
		echo "<td align=\"center\">".$data1['industry']."</td>";
		echo "<td align=\"center\">".$data1['smc']."</td>";
		echo "<td align=\"center\">".$data1['beta']."</td>";
	//	echo "<td align=\"center\">".$data1['errorfnc']."</td>";
		echo "</tr>";
	}
?>
</tbody>
</table>
</div>
</div>
</div>
<div class="col-sm-1"</div>
</div>
</form>
<script src="//code.jquery.com/jquery-2.1.4.min.js"></script> 
<script src="//rawgit.com/christianbach/tablesorter/master/jquery.tablesorter.min.js"></script> 
<script>
        $("#corplist").tablesorter();
</script>
</body>
</html>

