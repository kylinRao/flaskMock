drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);

drop table if exists comments;
create table comments (
  id integer primary key autoincrement,
  bookId integer,
  bookPage integer,
  commentOwnerId integer,
  comment string not null

);