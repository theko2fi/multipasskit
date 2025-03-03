FROM python:3.10

LABEL maintainer="Theko2Fi"

WORKDIR /code

# COPY ./ /code

COPY ./requirements.txt /code/requirements.txt

COPY ./requirements-api.txt /code/requirements-api.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -r /code/requirements-api.txt

# RUN cd /code && pip install -e .

RUN pip install git+https://github.com/theko2fi/multipasskit.git@develop

EXPOSE 9990

CMD ["multipasskit", "run-api"]