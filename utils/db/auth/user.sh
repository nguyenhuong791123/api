#!/bin/bash
psql -h sc-p-db -U postgres -d scapp << "EOSQL"
CREATE TABLE auth_users (
        id SERIAL NOT NULL, 
        name VARCHAR(200), 
        mail VARCHAR(200), 
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        PRIMARY KEY (id)
);
EOSQL
