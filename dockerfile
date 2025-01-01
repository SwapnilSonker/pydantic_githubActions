#initializing the base image
FROM python:3.9.13-slim 

#setting the working directory
WORKDIR /app

#copying the required files only
COPY requirements.txt .

#installing the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy the rest of the files
COPY . .

#exposing the port
EXPOSE 5000

#running the application
CMD ["python", "main.py"]