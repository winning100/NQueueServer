<?php
/*
request method: post
data: 
client_id
restaurant_id


return
1: success
-1: database error
-2: not on top of the queue
-9: can not connect to database

Example1:
1
check out successfully

Example2:
-9
Error: can't connect to database

Example3:
-2
can't check out. not on the top of the queue


*/

require_once ('include/db_function.php');

$client_id = $_POST['client_id'];
$restaurant_id = $_POST['restaurant_id'];
$force = $_POST['force'];

if ($force == "true")
    $force = true;
else
    $force = false;

$db = new mysqli('localhost','NQ','abc123','NQ_database');

if (mysqli_connect_errno()){
echo "-9\n";
echo "Error: could not connect to database\n";
exit;
}

$check_out_result = checkOut($db, $client_id, $restaurant_id, $force);
echo $check_out_result;
echo "\n";

if ($check_out_result == 1){
echo "check out successfully\n";
}
elseif ($check_out_result == -2)
echo "can not check out, you are not on the top\n";
elseif ($check_out_result == -1)
echo "can not check out, database error\n";
else
echo 'unknown error happens';
?>
