select location, date, new_cases, sum(cast(new_cases as float)) OVER (Partition by location order by location, date) as rollingCases
from covid..Sheet$
order by location, date
 