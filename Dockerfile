FROM python:3

RUN mkdir -p /usr/src/ssm

WORKDIR /usr/src/ssm

ADD . .

RUN pip install .

ENTRYPOINT [ "ssm" ]

CMD [ "--help" ]