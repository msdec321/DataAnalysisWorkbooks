select location, date, population, new_cases, new_deaths, total_cases , total_deaths, cast(total_cases as float)/population as caseRate,  cast(total_deaths as float)/population as deathRate, cast(total_deaths as float)/cast(total_cases as float) as deathCaseRatio
from covid..Sheet$
order by location, date