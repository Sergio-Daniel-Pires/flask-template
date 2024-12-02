FROM python:3.12-slim

ENV PYTHONPATH "${PYTHONPATH}:/{{ project_name }}"

WORKDIR /{{ project_name }}

COPY pyproject.toml ./

RUN pip install .
