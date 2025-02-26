FROM python:3.11-slim
WORKDIR /app

# Copy deps file and install
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

# Copy src
COPY src ./src

EXPOSE 8080

CMD ["python", "src/main.py"]
