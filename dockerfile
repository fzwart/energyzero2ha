FROM alpine:latest
RUN apk update && apk add --no-cache python3
RUN python3 -m venv /opt/venv && /opt/venv/bin/python3 -m pip install --upgrade pip
WORKDIR /opt/venv
COPY requirements.txt .
RUN . bin/activate && pip3 install -r ./requirements.txt
COPY config.yaml .
COPY run_energyzero.sh /etc/periodic/hourly/
COPY energyzero.py .
ENTRYPOINT crond -f -d8
