select avg(rating) as average_rating
from ratings
where movie_id in
(select id from movies
where year = '2012');
