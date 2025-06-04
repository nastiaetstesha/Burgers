# для сервера
# FROM python:3.10-slim

# WORKDIR /app
# RUN apt-get update && apt-get install -y \
#     curl \
#     unzip \
#     git \
#     gcc \
#     libjpeg-dev \
#     zlib1g-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# # 33b76eb0cbf7f281409ad79fc5cf37a660891dbbab3d5f46dc4baa4f5eb0be0a v - 1.0.0
# ADD --checksum=sha256:33b76eb0cbf7f281409ad79fc5cf37a660891dbbab3d5f46dc4baa4f5eb0be0a \
#   https://github.com/nastiaetstesha/Burgers/archive/refs/tags/1.0.0.zip /tmp/app.zip

# ENV PYTHONUNBUFFERED=1

# RUN unzip /tmp/app.zip && \
#     rm -rf ./assets ./bundles-src ./foodcartapp ./places ./restaurateur ./star_burger ./templates && \

#     mv Burgers-*/* . && \
#     pip install --no-cache-dir -r requirements.txt && \
#     rm -rf /tmp/app.zip Burgers-*

# CMD ["gunicorn", "star_burger.wsgi:application", "--bind", "0.0.0.0:8000"]

# локально собираю

FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "star_burger.wsgi:application", "--bind", "0.0.0.0:8000"]
