<?php
/*
input method: post
data:
client_id
restaurant_id

return
>0: success
-1: client not in the database
-9: can not connect to the database

*/

require_once('include/db_function.php');

$db = new mysqli("localhost", "NQ", "abc123","NQ_database");

if (mysqli_connect_errno()){
echo "-9\n";
echo "can not connect to database";
exit;
}

$client_id = $_POST['client_id'];
$restaurant_id = $_POST['restaurant_id'];

$rank = queryRank($db, $client_id, $restaurant_id);

echo $rank;

?>
