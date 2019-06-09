/*List all the pairs of customer and scooter IDs that have never occurred together in any rental reservations. 
In other words, we want the pairs of customers and scooter such that the customer has never rented the scooter. 
Hint: customers who have never rented any scooters, should still be accounted for */
select cs.id,sc.id from es.customer as cs CROSS JOIN es.scooters as sc EXCEPT 
select customer_id,scooter_id from es.rental_reservations;