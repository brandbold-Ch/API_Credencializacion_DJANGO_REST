import requests

endpoint = "http://127.0.0.1:8000/cuatrimestres/"


def insert():

    for i in range(1, 10):
        data = {
            "numero_cuatrimestre": str(i)
        }
        requests.post(endpoint, data)


insert()
