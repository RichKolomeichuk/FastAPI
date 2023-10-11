FROM Python:3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

RUN pip3 install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . .

CMD ("uvicorn", "main:app", "--reload")