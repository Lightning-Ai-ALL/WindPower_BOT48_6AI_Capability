FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY combined_transformer.py .
COPY missions/ ./missions/
COPY governance/ ./governance/

ENV MODE=SIMULATION_ONLY
ENV MARS_MISSION_ENABLED=true
ENV POLL_INTERVAL=30

CMD ["python", "combined_transformer.py"]
