-- Create onshore_oil_gas table and check it out
CREATE TABLE onshore_oil_gas (
facility_id INT,
facility_name VARCHAR,
basin VARCHAR,
city VARCHAR,
state VARCHAR,
zip_code INT,
primary_naics_code INT,
industry_type_subpart VARCHAR,
total_emissions_2020 NUMERIC,
total_emissions_2019 NUMERIC,
total_emissions_2018 NUMERIC,
total_emissions_2017 NUMERIC,
total_emissions_2016 NUMERIC,
total_emissions_2015 NUMERIC,
total_emissions_2014 NUMERIC,
total_emissions_2013 NUMERIC,
total_emissions_2012 NUMERIC,
total_emissions_2011 NUMERIC,
	PRIMARY KEY (facility_id)
);

SELECT * FROM onshore_oil_gas;

SELECT COUNT(facility_id) 
FROM onshore_oil_gas;

DROP TABLE onshore_oil_gas;

-- Create direct_emitters table and check it out
CREATE TABLE direct_emissions (
facility_id INT,
facility_name VARCHAR,
city VARCHAR,
state VARCHAR,
zip_code INT,
primary_naics_code INT,
industry_type_subpart VARCHAR,
industry_type_sector VARCHAR,
total_emissions_2020 NUMERIC,
total_emissions_2019 NUMERIC,
total_emissions_2018 NUMERIC,
total_emissions_2017 NUMERIC,
total_emissions_2016 NUMERIC,
total_emissions_2015 NUMERIC,
total_emissions_2014 NUMERIC,
total_emissions_2013 NUMERIC,
total_emissions_2012 NUMERIC,
total_emissions_2011 NUMERIC,
	PRIMARY KEY (facility_id)
);

SELECT * FROM direct_emissions;

SELECT COUNT(facility_id) 
FROM direct_emissions;

DROP TABLE direct_emissions;