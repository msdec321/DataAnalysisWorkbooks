--Select *
--From PortfolioProject..covid_deaths
--order by 3, 4

--Select *
--From PortfolioProject..covid_vaccinations
--order by 3, 4

--Select data to be used

Select Location, Date, total_cases, new_cases, total_deaths, population
From covid..Sheet$
order by 1,2

-- Looking at total cases vs total deaths
-- Shows likelyhood of dying if contract Covid in your country

Select Location, Date, total_cases, total_deaths, (total_deaths)/(total_cases)*100 as deathPercentage
From covid..Sheet$
Where location like '%states%'
order by 1,2


-- Looking at total cases vs population

Select Location, Date, total_cases, population, (total_cases)/(population)*100 as casesPercentage
From covid..Sheet$
Where location like '%states%'
order by 1,2


-- Highest infection rates by country

Select Location, max(total_cases) as HighestInfectionCount, population, max((total_cases)/(population))*100 as PercentInfected
From covid..Sheet$
group by population, location
order by PercentInfected desc


-- Countries with highest death count per capita

Select Location, max(cast(Total_deaths as int)) as TotalDeathCount
From covid..Sheet$
where continent is not null
group by location
order by TotalDeathCount desc


-- Break down by continent instead of location

Select Continent, max(cast(Total_deaths as int)) as TotalDeathCount
From covid..Sheet$
where continent is not null
group by continent
order by TotalDeathCount desc


-- Showing locations in North America with highest death count

Select location, max(cast(Total_deaths as int)) as TotalDeathCount
From covid..Sheet$
where continent like 'North America'
group by location
order by TotalDeathCount desc


-- Global data

Select date, sum(new_cases) as cases, sum(cast(new_deaths as int)) as deaths, sum(cast(new_deaths as int))/sum(new_cases)*100 as deathPercentage, sum(new_cases)/sum(population)*100 as casesPerCapitaPercentage
From covid..Sheet$
where continent is not null
group by date
order by 1 desc


-- Look at total population vs vaccinated

Select b.continent, b.location, b.date, b.population, a.new_vaccinations,

--sum(convert(int, a.new_vaccinations)) OVER (Partition by b.location ORDER BY b.location, b.date)
From covid..Sheet$ as a
Join covid..Sheet$ as b
On a.location = b.location and a.date = b.date
where a.new_vaccinations is not null
order by 2,3