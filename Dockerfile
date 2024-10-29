# Use a minimal Python base image
FROM python:3.11-slim

# Add a new group and user before all
RUN addgroup trade \
    && adduser --disabled-password --gecos "" paca \
    && adduser paca trade

# Set environment variables to avoid warnings about script locations
ENV PATH="/home/paca/.local/bin:$PATH"

# Switch to a less privileged user
USER paca

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install all dependencies in one step without caching build artifacts
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY telegram_bot.py ./
COPY telegram_client.py ./
COPY common.py ./
COPY investor_agent/ ./investor_agent/

# Run the Python script
CMD ["python3", "./telegram_bot.py"]
