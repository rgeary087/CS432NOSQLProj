FROM neo4j

RUN apt-get update && \ 
    apt-get install -yq --no-install-recommends \
    nano-tiny \
    python \
    python3-pip \
    vim-tiny && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install poetry

COPY . .

ENV NEO4J_AUTH=neo4j/test

RUN echo "hello  world"