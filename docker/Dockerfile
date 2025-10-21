FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
RUN pip install --upgrade pip && pip install -e .[openai]
COPY src /app/src
COPY sample_data /app/sample_data
