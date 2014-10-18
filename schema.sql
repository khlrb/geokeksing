drop table if exists kekse;
create table kekse (
	id integer primary key autoincrement,
	title text not null,
	creator text not null,
	description text not null,
	latitude text not null,
	longitude text not null,
	secret text not null unique
);	
