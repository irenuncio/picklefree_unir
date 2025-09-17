/*********************************************************************
CREACION DE LA BD PICKLEFREE Y EL USUARIO PICKLEFREE_OWNER PARA DJANGO 
*********************************************************************/

-- Borra la base de datos picklefree si ya existe
DROP DATABASE IF EXISTS picklefree;

-- Borra el usuario picklefree_owner si ya existe
DROP USER IF EXISTS picklefree_owner;

-- Crea un usuario picklefree_owner para Django
CREATE USER picklefree_owner WITH ENCRYPTED PASSWORD 'Rio+Congelado8826';

-- Pone a picklefree_owner los parámetros recomendados por Django
ALTER USER picklefree_owner SET client_encoding TO 'utf8';
ALTER USER picklefree_owner SET default_transaction_isolation TO 'read committed';
ALTER USER picklefree_owner SET timezone TO 'UTC';

-- Crea la base de datos con picklefree_owner como propietario
CREATE DATABASE picklefree OWNER picklefree_owner;
