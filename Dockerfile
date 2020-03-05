FROM python:3

RUN mkdir -p /usr/src/ssm

WORKDIR /usr/src/ssm

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

RUN pip install --editable .

ENTRYPOINT [ "ssm" ]

CMD [ "--help" ]