create table if not exists questions (
  id integer primary key not null unique,
  question varchar(1000),
  answer varchar(500)
);

create table if not exists quizadmin (
  pw varchar(250) unique,
  role text
);
