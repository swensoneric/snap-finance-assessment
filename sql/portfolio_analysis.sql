"-- SQL queries for portfolio analysis"  

select * from snap_application_details limit 5;

select * from snap_application_outcomes limit 5;

-- check dupes
SELECT application_id,
       COUNT(*) AS row_count
FROM snap_application_cleaned
GROUP BY application_id
HAVING COUNT(*) > 1;

-- confirm unique apps
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT application_id) AS distinct_apps
FROM snap_application_cleaned;

-- check for multi-outcome apps
SELECT application_id,
       COUNT(DISTINCT payoff_type) AS payoff_types
FROM snap_application_cleaned
GROUP BY application_id
HAVING COUNT(DISTINCT payoff_type) > 1; 

-- check for orphans (outcomes w/o apps)
SELECT application_id
FROM snap_application_cleaned
WHERE funded_amt IS NULL
  AND payoff_type IS NOT NULL;

-- only funded apps have amounts?
SELECT application_id, application_status, funded_amt
FROM snap_application_cleaned
WHERE funded_amt IS NOT NULL
  AND application_status NOT IN ('APPROVED', 'COMPLETE');


-- check one funding per app
SELECT application_id,
       COUNT(DISTINCT funded_dt) AS fund_events
FROM snap_application_cleaned
GROUP BY application_id
HAVING COUNT(DISTINCT funded_dt) > 1;

-- overview 
SELECT
  AVG(funded_amt) AS avg_funded,
  SUM(funded_amt) AS total_funded,
  AVG(fpd_30::int) AS fpd_30_rate,
  COUNT(*) FILTER (WHERE funded_amt > 0) AS funded_count,
  COUNT(*) AS total_apps
FROM snap_application_cleaned;

-- overview 2
SELECT
    COUNT(*) AS total_apps,
    COUNT(*) FILTER (WHERE funded_amt > 0) AS funded_apps,
    ROUND(AVG(funded_amt)) AS avg_funded_amt,
    ROUND(SUM(funded_amt)) AS total_funded_amt,
    ROUND(AVG(fpd_30::int)::numeric, 4) AS fpd_30_rate,
    ROUND(AVG(fpd_60::int)::numeric, 4) AS fpd_60_rate
FROM snap_application_cleaned;


