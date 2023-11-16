ARG PORT=8080

FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy and install the dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the files
COPY . .

# Expose the port (optional - this is for documentation purposes)
EXPOSE 8080

# Use the value of the PORT environment variable if available, default to 8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]