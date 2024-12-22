# Usa un'immagine Python ufficiale
FROM python:3.12-slim

# Installa dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    curl \
    && apt-get clean

# Configura il binario di ImageMagick per MoviePy
ENV IMAGEIO_IMAGEMAGICK_BINARY=/usr/bin/magick

# Crea la directory per l'applicazione
WORKDIR /app

# Copia i file del progetto
COPY . /app

# Installa le dipendenze Python e specifica versioni compatibili
RUN pip install --no-cache-dir Flask==2.2.3 Werkzeug==2.2.3 && \
    pip install --no-cache-dir -r requirements.txt

# Espone la porta del server Flask
EXPOSE 5001

# Comando per avviare l'app
CMD ["python", "app.py"]


