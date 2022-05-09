create table if not exists questions(
	id int primary key unique auto_increment,
	question varchar(1000) not null,
  answer varchar(500) not null
);
create table if not exists quizadmin (
	pw varchar(250) unique,
	role enum('admin','database_manager')
);
