<!DOCTYPE html>
<?php
session_start();
if(!isset($_SESSION['member']))
{
 header("Location: login.php");
 exit;
}
$dsn = null;
include_once 'db_data.php';

$companyn = $_GET["name"];
?>
<html>
<head>
<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
<script type="text/javascript" src="js/tablesorter-master/jquery-latest.js"></script> 
<script type="text/javascript" src="js/tablesorter-master/jquery.tablesorter.js"></script> 
<script type="text/javascript">
$(document).ready(function()
        {
                $("#corplist").tablesorter();
        }
);
</script>

<title> <?php echo $companyn ?> Company Profile </title>

</head>
<body>

<p> <?php echo $companyn ?> Company Profile - For Future</p>
<a href="logout.php"><p>Logout</p></a>

<?php
	$record1 = $databaseConnection1->prepare('SELECT * FROM ticklist WHERE tick = :tick');
	$record1->bindParam(':tick', $companyn, PDO::PARAM_STR);
	$record1->execute();
	echo "<table border=1>";
	echo "<tr>";
	echo "<th>Name</th>";
	echo "<th>Enabled</th>";
	echo "<th>Status</th>";
	echo "<th>Error Functions</th>";
	echo "</tr>";
	while($data1 = $record1->fetch(PDO::FETCH_ASSOC)){
		echo "<tr>";
		echo "<td align=\"center\">".$data1['tick']."</td>";
		if ($data1['enabled'] == 0){
			echo "<td align=\"center\"><img src=\"img/check.png\"></td>";
		} else {
			echo "<td align=\"center\"><img src=\"img/error.png\"></td>";
		}

		if ($data1['status'] == 0) {
			echo "<td align=\"center\"><img src=\"img/check.png\"></td>";
		} else {
			echo "<td align=\"center\"><img src=\"img/error.png\"></td>";
		}
		echo "<td align=\"center\">".$data1['errorfnc']."</td>";
		echo "</tr>";
		echo "</table>";
	}
?>
<br>
<br>
<?php

$link="https://ca.finance.yahoo.com/q?s=".$companyn;

$link2="http://amigobulls.com/stocks/".$companyn."/income-statement/quarterly";
?>
<table border=2>
	<tr>
	<td> Yahoo </td>
	<td><?php echo '<a href="'.$link.'" rel=\"external\"> link </a>'; ?></td>
	</tr>
	<tr>
	<td> Amigo </td>
	<td><?php echo '<a href="'.$link2.'" rel=\"external\"> link </a>'; ?></td>
	</tr>
</table>
</body>
</html>

