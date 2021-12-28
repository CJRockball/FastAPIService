FROM continuumio/anaconda3:2020.11 
#python:3.8-slim

WORKDIR /mapp

COPY requirements.txt /mapp/requirements.txt

RUN pip install -r /mapp/requirements.txt

COPY . /mapp/

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
ENTRYPOINT ["python", "app/main.py"]