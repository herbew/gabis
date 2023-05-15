-- Create User Database
CREATE USER ugabis WITH ENCRYPTED PASSWORD 'PwDgabisSatu1Dua3';

-- Create Database
CREATE DATABASE db_gabis;

GRANT ALL ON ALL TABLES IN SCHEMA public to ugabis;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to ugabis;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to ugabis;