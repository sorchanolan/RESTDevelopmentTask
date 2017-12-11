import requests
from flask_restful import Resource, Api
from flask import Flask, request

GET_WORK_URL = "http://127.0.0.1:5000"
ADD_WORKER_URL = "http://127.0.0.1:5000/add_worker"

class Worker(object):
	def __init__(self):
		self.worker_id = register_worker(self)


def register_worker(Worker):
    response = requests.get(ADD_WORKER_URL)
    worker_id = response.json()['new_worker']
    print 'Worker id assigned: {0}'.format(worker_id)
    return worker_id

if __name__ == '__main__':
    worker = Worker()

