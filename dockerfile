FROM python:3.11-alpine

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install required packages
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the script
COPY exporter.py /app/

# Expose the metrics port
EXPOSE 8000

ENTRYPOINT ["exporter", "main.py"]
