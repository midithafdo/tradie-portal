ARG py_version=3.8.11-slim-buster
FROM python:${py_version}

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y libsnappy-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements/*.txt /app/requirements/
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements/base.txt

COPY tradie_portal/ /app/tradie_portal/
COPY utils/ /app/utils/
COPY *.py /app/
COPY README.md /app/

ENTRYPOINT ["python", "-u", "main.py"]
