FROM python:3.7-slim-buster


# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Render uses dynamic PORT)
EXPOSE 10000

# Run your app
CMD ["python", "application.py"]
