FROM python:3.11.3-slim-buster
COPY . .
RUN pip3 install -r requirements.txt
CMD python dxtracter.py