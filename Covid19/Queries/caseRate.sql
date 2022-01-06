With CasesOverPop (location, date, population, new_cases, new_deaths, rollingCases, total_deaths)
as
(
select location, date, population, new_cases, new_deaths, sum(cast(new_cases as float)) OVER (Partition by location order by location, date) as rollingCases, total_deaths
from covid..Sheet$
-- DO NOT USE ORDER BY HERE
)
select *, (rollingCases/population)*100 as caseRate
from CasesOverPop
order by location, date