<?php
/*
request method: post
data:
restaurant_id
phone_number

return:
-9: can not connect to database
>= 0: check in successfully
-1: database error
-2: client already in the queue
-3: insert records into database error

Example 1:
5
check in successfully!
4
your rank is 4

Example 2:
-9
Error: Couldn't connect to database

Example 3:
-2
check in fails -2
*/
require_once('include/db_function.php');
?>
<?php
//$client_id = $_POST['client_id'];
$phone = $_POST['phone_number'];
$restaurant_id = $_POST['restaurant_id'];


$db = new mysqli ('localhost', 'NQ', 'abc123','NQ_database');

/*$db = new mysqli (SAE_MYSQL_HOST_M.':'.SAE_MYSQL_PORT, 
                  SAE_MYSQL_USER, 
                  SAE_MYSQL_PASS,
                  SAE_MYSQL_DB
                 );
*/
if (mysqli_connect_errno()){
	echo '-9';
	echo "\n";
	echo 'Error: Could not connect to database. Please try again later.</info>\n';
	
	exit;
}

$check_result = checkIn($db,$restaurant_id,$phone);

echo "$check_result\n";

if ($check_result >= 0)
	echo "check in successfully!\n";
	else{
		echo "check in fails $check_result\n";
		exit;
	}
$rank = queryRank($db, $check_result,$restaurant_id);

echo "$rank\n";
echo "your rank is $rank";



?>
