FROM neo4j

RUN apt-get update && \ 
    apt-get install -yq --no-install-recommends \
    nano-tiny \
    python3 \
    python3-pip \
    vim-tiny && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install poetry

RUN apt-get update && \ 
    apt-get install -yq --no-install-recommends \
    vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .

RUN poetry install

COPY src .

ENV NEO4J_AUTH=neo4j/test

