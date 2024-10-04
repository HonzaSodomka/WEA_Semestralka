# Použijeme oficiální Python image
FROM python:3.9-slim

# Nastav pracovní adresář
WORKDIR /app

# Zkopíruj requirements.txt a nainstaluj závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj ostatní soubory aplikace
COPY . .

# Exponuj port 8007 (port, na kterém běží Flask aplikace)
EXPOSE 8007

# Spusť Flask aplikaci na portu 8007
CMD ["python", "app.py"]
