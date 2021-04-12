create database demo character set utf8mb4 collate utf8mb4_unicode_ci;
create user demo@'%' identified by 'Demo123!';
grant all privileges on demo.* to demo@'%';
set global validate_password_policy=0;
