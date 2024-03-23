select movies.title from movies
where movies.id in (select stars.movie_id from stars
join people on people.id = stars.person_id
where people.name = 'Bradley Cooper')
and
movies.id in (select stars.movie_id from stars
join people on people.id = stars.person_id
where people.name = 'Jennifer Lawrence');

