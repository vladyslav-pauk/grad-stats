FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app/viewer
RUN pip install --no-cache-dir -r viewer/requirements.txt
EXPOSE 5000
CMD ["python", "viewer/src/app.py"]
