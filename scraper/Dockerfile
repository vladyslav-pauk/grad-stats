FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app/scraper
RUN pip install --no-cache-dir -r scraper/requirements.txt
EXPOSE 5000
CMD ["python", "-m", "scraper"]
