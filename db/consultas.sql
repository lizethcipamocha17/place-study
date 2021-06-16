-- Consulta de trae contenidos por colegios

select c.name, s.school_id, s.school_name, u.first_name from content c
inner join school s on c.school_id = s.school_id
inner join public.user u on u.school_id  = s.school_id
where u.school_id = 1   ;

-- consulta de docentes por colegios

select u.first_name, u.last_name, s.school_name  from public."user"  u
inner join school s on s.school_id = u.school_id
where s.school_id = 2 and u.type_user = 'TCHR';

-- mostrar contenido según el colegio del usuario logueado y comentarios


select u.first_name,u.last_name, cm.text, c.name,s.school_name , c.school_id from school s
inner join content c on s.school_id = c.school_id
inner join comment cm on c.content_id = cm.content_id
inner join public."user" u on cm.user_id = u.user_id
where user_id = 4;

-- like por contenidos de un colegio
select s.school_name,c.name,c.like from school s
inner join content c on s.school_id = c.school_id

-- traer likes por contenido
select c.name, u.username, l."like" , count(l."like") from "user" u
inner join "like" l on u.user_id = l.user_id
inner join content c on c.content_id = l.content_id

where c.content_id = 1
Group by l.user_id, l.content_id, l."like", c.name, u.username;

-- traer likes por contenido
select l.content_id, count(l."like")
from "like" l
where l.content_id = 1
Group by l.content_id

