select location, max(new_cases) as maxNewCases
from covid..Sheet$
group by location
order by location

-- Rolling variables
select location, date, new_cases, sum(cast(new_cases as float)) OVER (Partition by location order by location, date) as rollingCases
from covid..Sheet$
order by location, date


-- Using CTEs
With CasesOverPop (location, date, new_cases, population, rollingCases)
as
(
select location, date, new_cases, population, sum(cast(new_cases as int)) OVER (Partition by location order by location, date) as rollingCases
from covid..Sheet$
-- DO NOT USE ORDER BY HERE
)
select *, (rollingCases/population)*100
from CasesOverPop


-- Using temp tables
Drop table if exists #PercentPopCases
Create table #PercentPopCases
(location nvarchar(255), date datetime, new_cases numeric, population numeric, rollingCases numeric)

Insert into #PercentPopCases
select location, date, new_cases, population, sum(cast(new_cases as int)) OVER (Partition by location order by location, date) as rollingCases
from covid..Sheet$

select *, (rollingCases/population)*100 as rollingCasesPopPercentage
from #PercentPopCases
order by location, date


-- Create a view (virtual table) using create view <name> as <SQL statement>
Use covid --Without this line, the view is made in the Master database
Go

Create view rollingCasesView as
select location, date, new_cases, sum(cast(new_cases as int)) OVER (Partition by location order by location, date) as rollingCases
from covid..Sheet$
-- ORDER BY cannot be used in views