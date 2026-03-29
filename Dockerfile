FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Hugging Face Spaces specifically look for port 7860
EXPOSE 7860

# This command runs your baseline inference script to prove the env works 
# and then keeps the container alive for the Hugging Face API
CMD ["python", "inference.py"]