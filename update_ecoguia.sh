#!/bin/bash

echo "🔄 Guardando cambios locales..."
git stash save "Cambios locales antes de pull"

echo "📥 Actualizando repositorio desde GitHub..."
git pull origin main

echo "🔙 Restaurando cambios locales..."
git stash pop

echo "📦 Instalando dependencias del backend (Django)..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

echo "📦 Instalando dependencias del frontend (React)..."
cd frontend
npm install
cd ..

echo "✅ Proyecto actualizado y listo!"
