#!/bin/bash

# Script para crear una base de datos PostgreSQL con Docker

CONTAINER_NAME="fastapi_postgres"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="fastapi_db"
DB_PORT="5432"

echo "Iniciando contenedor PostgreSQL..."

docker run -d \
    --name $CONTAINER_NAME \
    -e POSTGRES_USER=$DB_USER \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -e POSTGRES_DB=$DB_NAME \
    -p $DB_PORT:5432 \
    -v fastapi_pg_data:/var/lib/postgresql/data \
    postgres:18-alpine

echo "✓ Contenedor PostgreSQL iniciado"
echo ""
echo "Detalles de conexión:"
echo "Host: localhost"
echo "Port: $DB_PORT"
echo "User: $DB_USER"
echo "Password: $DB_PASSWORD"
echo "Database: $DB_NAME"
echo ""
echo "Connection string: postgresql://$DB_USER:$DB_PASSWORD@localhost:$DB_PORT/$DB_NAME"