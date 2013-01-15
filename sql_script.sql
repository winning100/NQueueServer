CREATE TABLE q_info 
(
client_id int not null auto_increment primary key,
restaurant_id int not null,
phone char(15),
check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE restaurant_info
(
restaurant_id int not null primary key,
restaurant_name char(20),
restaurant_password

);
