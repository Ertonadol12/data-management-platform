FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create upload directory
RUN mkdir -p app/static/uploads

# Create a startup script that initializes database then runs the app
RUN echo '#!/bin/bash\n\
echo "Initializing database..."\n\
python -c "from app import create_app, db; from app.models import User, Upload, ProcessedFile, QualityMetrics, UserSession; app = create_app(); with app.app_context(): db.create_all(); print(\"Database tables created successfully\")"\n\
echo "Starting Gunicorn..."\n\
gunicorn run:app --bind 0.0.0.0:10000' > /start.sh && chmod +x /start.sh

EXPOSE 10000

CMD ["/start.sh"]