# 📊 Data Management Platform (DMP)

A full-stack web application for uploading, cleaning, analyzing, and managing data files.

## ✨ Features

- **User Authentication** - Secure login/register system
- **File Upload** - Drag & drop support for CSV, Excel, JSON
- **Data Preview** - View first 100 rows with column statistics
- **Data Cleaning** - Remove duplicates, fill missing values, standardize text
- **Quality Reports** - Generate detailed reports with charts
- **Upload History** - Track all your processed files
- **User Profile** - Manage account settings

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Flask |
| Database | SQLite / PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Charts | Chart.js |
| File Upload | Dropzone.js |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

# Clone the repository
git clone https://github.com/Ertonadol12/data-management-platform.git
cd data-management-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 init_db.py

# Run the application
python3 run.py

## Running Tests
pytest tests/ -v

## 👨‍💻 Author
Ermias Meseret-Data Engineer

## 📝 License
MIT License



