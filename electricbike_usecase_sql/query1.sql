/* List the name, model and battery_capacity of all scooters in city ’Copenhagen’ 
that have a rental reservation between noon of 08/07/2019 and midnight of 15/07/2019 (both inclusive) 
for a customer with an Android phone */
select sc.name,sc.model,sc.battery_capacity from es.scooters as sc 
INNER JOIN es.rental_reservations as rr ON sc.id = rr.scooter_id 
INNER JOIN es.customer as cs on rr.customer_id = cs.id 
where sc.city='Copenhagen' and rr.start_datetime < '2019-08-07 12:00:00' 
and rr.end_datetime < '2019-15-07 23:59:59' and LENGTH(cs.platform_token)=12;
