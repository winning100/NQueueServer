<?php

/*

return
>=0: insert successfully, the return value is the client id
-3 : insert database error
*/
function checkIn($db, $restaurant_id, $phone){


	$query = "INSERT INTO q_info 
		(restaurant_id,phone,check_in_time)
		Values ($restaurant_id, $phone,DEFAULT);
	         ";
	$result = $db->query($query);
//	echo "insert_id is $db->insert_id\n";

	if ($result)
		return $db->insert_id;   //this one is the client_id
	else 
		return -3;
}
/*
return
true: delete successfully
false: delete error
*/
function quit($db, $client_id, $restaurant_id){
	$query = "DELETE FROM q_info
		WHERE client_id = $client_id and restaurant_id = $restaurant_id";

	$result = $db->query($query);
	if ($result)
		return true;
	else
		return false;
}
/*
if force is true, the client doesn't have to be on top of the queue
return:
1 : success
-1: database error
-2: not on top of the queue
*/
function checkOut($db, $client_id, $restaurant_id,$force=false){
	if ($force){
		quit($db, $client_id, $restaurant_id);
		return 1; 
	}
	$rank = queryRank ($db, $client_id, $restaurant_id);
	if ($rank == 1){
		quit($db, $client_id, $restaurant_id);
		return 1;
	}
	elseif ($rank < 0)
		return -1;
	else
		return -2;
}

function queryRank($db, $client_id, $restaurant_id){
/*	$query = "SELECT * FROM q_info WHERE client_id = $client_id and restaurant_id = $restaurant_id;";

	$result = $db->query($query);

	if (!$result)
		return -1;
	//The client not in the database
	if ($result->num_rows == 0)
		return -1;

	for ($i = 0; $i < $result->num_rows; $i++){
		$row = $result->fetch_assoc();
		$q_id = $row['client_id'];
	}
*/

	$query = "SELECT * FROM q_info WHERE restaurant_id = $restaurant_id and client_id < $client_id";
//	$result->free();
	$result = $db->query($query);
	$rank = 1 + $result->num_rows;
	$result->free();
	return $rank;
}

?>
