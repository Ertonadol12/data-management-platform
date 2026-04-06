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

# Initialize database and run app in one command
CMD sh -c "python -c 'from app import create_app, db; from app.models import User, Upload, ProcessedFile, QualityMetrics, UserSession; app = create_app(); app.app_context().push(); db.create_all(); print(\"Database ready\")' && gunicorn run:app --bind 0.0.0.0:10000"