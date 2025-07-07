#!/bin/bash

echo "🔄 Revisando cambios locales..."

# Añade todos los cambios (modificados y nuevos)
git add .

# Haz commit automático con mensaje genérico (si hay cambios para commitear)
if git diff-index --quiet HEAD --; then
    echo "No hay cambios para commitear."
else
    git commit -m "Commit automático antes de pull para evitar conflictos"
fi

echo "📥 Actualizando repositorio desde GitHub..."
# Intenta hacer pull con merge
if git pull --no-rebase origin main; then
    echo "✅ Pull completado sin conflictos."
else
    echo "❌ Hubo conflictos durante el pull."
    echo "Por favor, resuelve los conflictos manualmente y luego haz git add y git commit."
    exit 1
fi

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
