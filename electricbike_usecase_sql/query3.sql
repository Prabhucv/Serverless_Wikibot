/* List the median rental period for Android and iPhone users respectively */
CREATE OR REPLACE FUNCTION _final_median(NUMERIC[])
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
 
CREATE AGGREGATE median1(NUMERIC) (
  SFUNC=array_append,
  STYPE=NUMERIC[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);
--https://wiki.postgresql.org/wiki/Aggregate_Median

select median1(CAST(durationInMinutes as INTEGER)) as Median_durationInMinutes,platform_type from (select ((DATE_PART('day', end_datetime::timestamp - start_datetime::timestamp) * 24 +DATE_PART('hour', end_datetime::timestamp - start_datetime::timestamp)) * 60 + DATE_PART('minute', end_datetime::timestamp - start_datetime::timestamp)) as durationInMinutes,
CASE WHEN LENGTH(cs.platform_token)=12 then 'ANDRIOD' WHEN LENGTH(cs.platform_token)=20 then 'IOS' else 'NA' END as platform_type 
from es.rental_reservations as rr 
INNER JOIN es.customer as cs on rr.customer_id = cs.id) dim group by platform_type;