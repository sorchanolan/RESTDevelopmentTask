import requests
from flask_restful import Resource, Api
from flask import Flask, request

WORKER_ID = ""
GET_WORK_URL = "http://127.0.0.1:5000"
ADD_WORKER_URL = "http://127.0.0.1:5000/add_worker"
REPO_URL = "https://github.com/sorchanolan/RESTDevelopmentTask"
commits_list = []
repo = None
count = 0

class Worker(object):
	def __init__(self):
		add_worker()
		self.running = True

	def steal_work(self):
		global count 

		while(self.running):
			response = requests.get(GET_WORK_URL, json={"worker_id": WORKER_ID})
			if response.json()['finished'] is True:
				self.running = False
				break
			else:
				commit = response.json()['commit']
				count += 1 
				self.execute_task(commit)

	def execute_task(self, commit):
		print "{0}".format(count)

def add_worker():
	global WORKER_ID
	response = requests.get(ADD_WORKER_URL)
	worker_id = response.json()['new_worker']
	print 'Worker id assigned: {0}'.format(worker_id)
	WORKER_ID = str(worker_id)

if __name__ == '__main__':
    worker = Worker()
    worker.steal_work() 

