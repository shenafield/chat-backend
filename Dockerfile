FROM python:3.10-slim
RUN pip install poetry
COPY pyproject.toml .
RUN poetry install
COPY * ./
EXPOSE 5000
CMD ["poetry", "run", "python", "serve.py"]