# Base image
FROM python:latest

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .


# Set the entrypoint command
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]