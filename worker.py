import requests, lizard, os

from git import Repo
from os import walk
from flask_restful import Resource, Api
from flask import Flask, request

WORKER_ID = ""
GET_WORK_URL = "http://127.0.0.1:5000"
ADD_WORKER_URL = "http://127.0.0.1:5000/add_worker"
REPO_URL = "https://github.com/parcel-bundler/parcel"
commits_list = []
repo = None
running = True

def steal_work():
	global count, running
	while(running):
		response = requests.get(GET_WORK_URL, json={"worker_id": WORKER_ID})
		print "{0}".format(str(response))
		commit = response.json()['commit']
		if response.json()['finished'] is True:
			print "Worker {0} finished".format(WORKER_ID)
			running = False
			break
		elif commit == "wait":
			#print "Worker {0} waiting...".format(WORKER_ID)
			pass
		else:
			execute_task(commit)

def execute_task(commit):
	complexity_sum = 0
	num_files = 0
	filenames = get_files(commit)
	for filename in filenames:
		complexity_sum += compute_cyclo_complex(filename)
		num_files += 1
	requests.post(GET_WORK_URL, json={'average_complexity': get_average(num_files, complexity_sum), 'worker_id': WORKER_ID, 'commit': commit})

def get_files(commit):
	git = repo.git
	git.checkout(commit)
	files = []
	for (dirpath, dirnames, filenames) in walk(path):
		for filename in filenames:
			if '.js' in filename:
				files.append(dirpath + '/' + filename)
	return files

def compute_cyclo_complex(file_name):
	file_info = lizard.analyze_file(file_name)
	return file_info.average_cyclomatic_complexity

def get_average(num_files, sum):
	if num_files is 0:
		return 0
	return sum / num_files


def add_worker():
	global WORKER_ID
	response = requests.get(ADD_WORKER_URL)
	worker_id = response.json()['new_worker']
	print 'Worker {0} assigned'.format(WORKER_ID)
	WORKER_ID = str(worker_id)

def get_repo():
	print 'Cloning repository {0} for worker {1}'.format(REPO_URL, WORKER_ID)
	if not os.path.exists(path):
		os.makedirs(path)
	if not os.listdir(path):
		repo = Repo.clone_from(REPO_URL, path)
	else:
		repo = Repo(path)
	return repo

if __name__ == '__main__':
	add_worker()
	path = "WorkerRepo_" + WORKER_ID
	repo = get_repo()
	steal_work() 

