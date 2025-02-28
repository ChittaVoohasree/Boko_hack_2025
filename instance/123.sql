select * from admin_credentials;
select * from files;
select * from notes;
select * from users;
select * from sqlite_schema;
create table reservation from
SELECT * FROM users WHERE username = '1' AND password = '' OR '1'='1';
SELECT * FROM users WHERE username = '1' AND password = ' OR '1'='1;
SELECT * FROM notes WHERE user_id in (SELECT id FROM users WHERE username = '1');
(SELECT user_id FROM users WHERE username = '1');