# Stable Python version nibe
FROM python:3.11-slim

# System e missing error wala file gulo jor kore install korbe
RUN apt-get update && apt-get install -y libpq-dev gcc

# App er folder setup
WORKDIR /app

# Python packages install korbe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Apnar bot er code copy korbe
COPY . .

# Bot chalu korbe
CMD ["python", "tg_bot.py"]
