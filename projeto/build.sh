#!/usr/bin/env bash
set -o errexit

echo "=== [1/4] Instalando dependências Python ==="
pip install -r requirements.txt

echo "=== [2/4] Instalando Node e buildando o React ==="
cd frontend
npm ci
npm run build
cd ..

echo "=== [3/4] Copiando build do React para django_min/spa/ ==="
rm -rf django_min/spa
mkdir -p django_min/spa
cp -r frontend/dist/. django_min/spa/

echo "=== [4/4] Django: migrate + collectstatic + seed ==="
cd django_min
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_catalogo
cd ..

echo "=== Build concluído ==="
