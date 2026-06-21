#!/bin/bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar migraciones
flask db upgrade

echo "Build completado exitosamente"
