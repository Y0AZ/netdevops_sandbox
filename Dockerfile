# Conteneurise l'outil : "ça marche chez moi" = "ça marche partout".
# En NetDevOps réel, on conteneurise souvent les outils d'automatisation
# pour garantir un environnement identique en local et en CI.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Par défaut : génère puis valide.
CMD ["sh", "-c", "python generate.py && python validate.py"]
