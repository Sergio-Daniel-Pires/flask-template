FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /project

COPY pyproject.toml README.md ./
COPY project ./project
RUN pip install .

COPY gunicorn.conf.py ./

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "project.wsgi:app"]
