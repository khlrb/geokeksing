drop table if exists kekse;
create table kekse (
	id integer primary key autoincrement,
	title text not null,
	creator text not null,
	description text not null,
	latitude text not null,
	longitude text not null,
	secret text not null unique,
	status integer default 1
);	
create table status (
	id integer primary key autoincrement,
	title text not null
);
insert into status (title) values ('aktiv');
insert into status (title) values ('inaktiv');
insert into status (title) values ('abgelaufen');
