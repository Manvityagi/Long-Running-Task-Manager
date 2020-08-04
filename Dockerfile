FROM python
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install django-cors-headers
COPY . /code/
