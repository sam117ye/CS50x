select avg(energy) as averege_energy from songs
join artists on songs.artist_id = artists.id
where artists.name = 'Drake';
