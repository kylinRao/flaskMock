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
  pageId integer,
  bookPage integer,
  commentOwnerId integer,
  comment string not null

);
drop table if exists books;
create table books (
  id integer primary key autoincrement,
  bookName string not null,
  bookFileType string not null,
  savedFile string not NULL

);