drop type if exists quiz_role cascade;
create type quiz_role as enum('admin','database_manager');

create table if not exists questions (
  id smallserial primary key unique,
  question varchar(1000) not null,
  answer varchar(500) not null
);
create table if not exists quizadmin (
  pw varchar(250) unique,
  role quiz_role
);