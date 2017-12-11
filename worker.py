import requests, lizard
from flask_restful import Resource, Api
from flask import Flask, request

WORKER_ID = ""
GET_WORK_URL = "http://127.0.0.1:5000"
ADD_WORKER_URL = "http://127.0.0.1:5000/add_worker"
REPO_URL = "https://github.com/sorchanolan/DistributedFileSystem"
commits_list = []
repo = None
count = 0

class Worker(object):

	def __init__(self):
		add_worker()
		self.running = True
		self.path = "WorkerRepo_" + WORKER_ID
		self.repo = get_repo(path)
		self.num_files = 0
		self.complexity_sum = 0


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
		complexity_sum = 0
		num_files = 0
		filenames = get_files(commit)
		for filename in filenames:
			sum_complexity += self.compute_cyclo_complex(filename)
			num_files += 1
		
        if num_files is 0:
        	avg_complexity = 0
        else:
        	avg_complexity = complexity_sum / num_files

    	requests.post(GET_WORK_URL, json={'average_complexity': avg_complexity})


	def get_files(self, commit):
		git = self.repo.git
		git.checkout(commit)
		files = []
		for (dirpath, dirnames, filenames) in walk(self.path):
			for filename in filenames:
				if '.java' in filename:
					files.append(dirpath + '/' + filename)
		return files


	def compute_cyclo_complex(self, file_name):
		file_info = lizard.analyse_file(file_name)
		return file_info.average_cyclomatic_complexity


def add_worker():
	global WORKER_ID
	response = requests.get(ADD_WORKER_URL)
	worker_id = response.json()['new_worker']
	print 'Worker id assigned: {0}'.format(worker_id)
	WORKER_ID = str(worker_id)

def get_repo(path):
	print 'Cloning repository {0}'.format(REPO_URL)
	if not os.path.exists(path):
		os.makedirs(path)
	if not os.listdir(path):
		repo = Repo.clone_from(REPO_URL, path)
	else:
		repo = Repo(path)
	return repo

if __name__ == '__main__':
    worker = Worker()
    worker.steal_work() 

