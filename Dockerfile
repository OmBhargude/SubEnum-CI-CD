FROM docker.io/library/python:3.9-slim-buster
WORKDIR /ap

# Copy subfinder (assuming it's in the same directory as the Dockerfile)
COPY subfinder /ap/  
# Copy the subfinder binary

# Copy your web application code
COPY . /ap/ 
# Copy the web app directory including app.py and templates

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set environment variables (if needed)
ENV PORT 5000
ENV DEBUG_PRINT "true"

CMD ["python3", "app.py"]
