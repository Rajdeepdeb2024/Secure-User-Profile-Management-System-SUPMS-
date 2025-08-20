create database Python_Project
use Python_Project 
show tables
CREATE TABLE cust_details (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    phone_number BIGINT NOT NULL,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
) AUTO_INCREMENT=1000;

select * from cust_details;

INSERT INTO cust_details (full_name, address, phone_number, user_id, password)
VALUES ('Sourav Kundu', '123 Park Street, Kolkata, West Bengal', 9876543211, 'sourav123', 'P@ssw0rd!');

truncate table cust_details;

select * from cust_details where user_id='RAJ45';
select * from cust_details WHERE user_id=sourav123