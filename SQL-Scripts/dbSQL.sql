select d.name as destination_name, avg(r.rating) as average_rating
from destination d
join review r on d.destinationid = r.destinationid
group by d.name
order by average_rating desc;



select u.userid, u.name, count(b.bookingid) as total_bookings
from user u
join booking b on u.userid = b.userid
group by u.userid, u.name
order by total_bookings desc;


select u.userid, u.name, count(r.reservationid) as total_reservations
from user u
join reservation r on u.userid = r.userid
group by u.userid, u.name
having count(r.reservationid) > 2;


select distinct u.name as username, h.city from user u join booking b on u.userid = b.userid join hotel h on b.hotelid = h.hotelid where h.city in (select city from destination where adminid = 1);


select roomtype, avg(cost) as average_cost
from booking
group by roomtype
order by average_cost desc;


select reviewtype, count(*) as total_reviews from review  group by reviewtype order by total_reviews desc;



select r.name as restaurantname, r.city, count(res.reservationid) as totalreservations from restaurant r join reservation res on r.restaurantid = res.restaurantid join user u on res.userid = u.userid join favourite f on u.userid = f.userid join destination d on f.destinationid = (select destinationid from destination where city = r.city limit 1) group by r.restaurantid, r.name, r.city order by totalreservations desc;


select r.name, r.city from restaurant r where not exists (select 1 from reservation res join booking b on res.userid = b.userid join hotel h on b.hotelid = h.hotelid where res.restaurantid = r.restaurantid and h.city = r.city) order by r.city, r.name;


select d.name as destinationname, count(distinct h.hotelid) as numhotels, count(distinct r.restaurantid) as numrestaurants from destination d left join hotel h on d.city = h.city left join restaurant r on d.city = r.city group by d.destinationid, d.name having numhotels > 0 and numrestaurants > 0 order by numhotels desc, numrestaurants desc;


select name, email from user where userid in (select distinct b.userid from booking b join hotel h on b.hotelid = h.hotelid where h.city in (select d.city from favourite f join destination d on f.destinationid = d.destinationid where f.userid = b.userid));