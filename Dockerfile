FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p app/static/uploads

# Create a Python script for database initialization
RUN echo 'from app import create_app, db; from app.models import User, Upload, ProcessedFile, QualityMetrics, UserSession; app = create_app(); app.app_context().push(); db.create_all(); print("Database tables created successfully")' > init_db_container.py

# Run database init then start gunicorn
RUN echo 'python init_db_container.py && gunicorn run:app --bind 0.0.0.0:10000' > /start.sh && chmod +x /start.sh

EXPOSE 10000

CMD ["/start.sh"]