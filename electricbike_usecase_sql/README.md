# TonsserChallenge
Tonsser Challenge - Electric Bike UseCase - 3 Queries  

## Query 1
List the name, model and battery_capacity of all scooters in city ’Copenhagen’ that have a rental reservation between noon of 08/07/2019 and midnight of 15/07/2019 (both inclusive) for a customer with an Android phone.
  > select sc.name,sc.model,sc.battery_capacity from es.scooters as sc 
INNER JOIN es.rental_reservations as rr ON sc.id = rr.scooter_id 
INNER JOIN es.customer as cs on rr.customer_id = cs.id 
where sc.city='Copenhagen' and rr.start_datetime < '2019-08-07 12:00:00' 
and rr.end_datetime < '2019-15-07 23:59:59' and LENGTH(cs.platform_token)=12;
### Approach 
* Inner Join is obvious choice for these kind of queries where the join is required only to get the date time information
* Date, Time & City are Straight forward condition values 

## Query 2 
List all the pairs of customer and scooter IDs that have never occurred together in any rental reservations. In other words, we want the pairs of customers and scooter such that the customer has never rented the scooter. Hint: customers who have never rented any scooters, should still be accounted for.
  > select cs.id,sc.id from es.customer as cs CROSS JOIN es.scooters as sc EXCEPT 
select customer_id,scooter_id from es.rental_reservations;

### Approach 
* Cross Join is used to get all the possible combination of customerid and scooterid subtracted with rental reservation table
* Though Cross Join is used in this query, it is not advisable for querying huge number of rows 

### Assumptions 
* If a customer rented only one scooter out of ten, resultset should include combination of this one customer with remaining 9 scooters. Applicable to all customer including the ones who never rented any scooter

### Tests
* Count Validation 

## Query 3 
List the median rental period for Android and iPhone users respectively.
#### Stored Procedure
  > CREATE OR REPLACE FUNCTION _final_median(NUMERIC[])
   RETURNS NUMERIC AS
$$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$$
LANGUAGE 'sql' IMMUTABLE;
 
 #### Function
  > CREATE AGGREGATE median1(NUMERIC) (
  SFUNC=array_append,
  STYPE=NUMERIC[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);

#### Query
  > select median1(CAST(durationInMinutes as INTEGER)) as Median_durationInMinutes,platform_type from (select ((DATE_PART('day', end_datetime::timestamp - start_datetime::timestamp) * 24 +DATE_PART('hour', end_datetime::timestamp - start_datetime::timestamp)) * 60 + DATE_PART('minute', end_datetime::timestamp - start_datetime::timestamp)) as durationInMinutes,
CASE WHEN LENGTH(cs.platform_token)=12 then 'ANDRIOD' WHEN LENGTH(cs.platform_token)=20 then 'IOS' else 'NA' END as platform_type 
from es.rental_reservations as rr 
INNER JOIN es.customer as cs on rr.customer_id = cs.id) dim group by platform_type;

### Approach 
* Using stored procedure for calculating Median as we do not have inbuild functions to solve this purpose
* length of the platform token clearly shows the type of operating system used by the customer. so using length function to determine the platform type 
* Inner Join is obvious choice for these kind of queries where the join is required only to get the date time information

### Assumptions
* Duration in Minutes would be good choice as time spans across days 
