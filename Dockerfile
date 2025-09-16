# ===============================
# Etapa base con Python 3.11.5
# ===============================
FROM python:3.11.5-slim

# Crear usuario no root
RUN useradd -ms /bin/bash api-user

# Directorio de trabajo
WORKDIR /home/api-user/cervical_cancer_app

# Copiar requirements primero (mejora cacheo)
COPY requirements_app.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements_app.txt

# Crear solo carpeta save (assets y models se sobrescriben al copiar)
RUN mkdir -p /home/api-user/cervical_cancer_app/save

# Copiar los directorios necesarios
COPY ./assets /home/api-user/cervical_cancer_app/assets
COPY ./data/train_models /home/api-user/cervical_cancer_app/models
COPY ./scripts_app/ /home/api-user/cervical_cancer_app/

# Cambiar permisos
RUN chown -R api-user:api-user /home/api-user/cervical_cancer_app

# Cambiar a usuario no root
USER api-user

# Variables de entorno (rutas fijas)
ENV EXTERNAL_IMAGES_PATH=/home/api-user/cervical_cancer_app/assets \
    save_path=/home/api-user/cervical_cancer_app/save \
    model_path=/home/api-user/cervical_cancer_app/models/best.pt

# Exponer puerto
EXPOSE 8050

# Ejecutar aplicación
CMD ["python", "server_app.py"]
