CREATE DATABASE sensor
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_CA.UTF-8'
       LC_CTYPE = 'en_CA.UTF-8'
       CONNECTION LIMIT = -1;

CREATE TABLE light
(
  "timestamp" timestamp without time zone NOT NULL,
  value real,
  CONSTRAINT light_pkey PRIMARY KEY ("timestamp")
)
WITH (
  OIDS=FALSE
);
