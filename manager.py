import os, sys

from git import Repo
from flask_restful import Resource, Api
from flask import Flask, request
from random import randint

NUM_WORKERS = 0
REPO_URL = "https://github.com/sorchanolan/DistributedFileSystem"
commits_list = []
commits_not_returned = []
commits_index = 0
repo = None
finished = False
results_list = []
results_map = dict()

app = Flask(__name__)
api = Api(app)

class Manager(Resource):

	def get(self): 
		global commits_list, commits_index, finished
		if NUM_WORKERS == int(num_workers_required):
			if commits_index < len(commits_list):
				print "Sending out commit {0}".format(commits_index)
				commit = commits_list[commits_index]
				commits_index += 1
			elif commits_index == len(commits_list) - 1:
				print "Commits sent out, {0} not returned".format(len(commits_not_returned))
				if len(commits_not_returned) > 0:
					commit = commits_list[randint(0, len(commits_not_returned) - 1)]
			else:
				print "Finished"
				commit = None
				finished = True
				print results_map
		else:
			print "Waiting, {0} workers out of {1}".format(NUM_WORKERS, num_workers_required)
			commit = "wait"
		return {"commit": commit, "finished": finished}


	def post(self):
		response = request.get_json()
		results_list.append(response['average_complexity'])
		commits_not_returned.remove(response['commit'])
		results_map[response['commit']] = response['average_complexity']
		print "{0} of {1} returned by {2}".format(response['average_complexity'], response['commit'], response['worker_id'])


class AddWorker(Resource):
	def get(self): 
		global NUM_WORKERS
		NUM_WORKERS += 1
		response = {"new_worker":NUM_WORKERS}
		print "New worker added: {0}".format(NUM_WORKERS)
		return response

def get_repo(path):
	print 'Cloning repository {0}'.format(REPO_URL)
	if not os.path.exists(path):
		os.makedirs(path)
	if not os.listdir(path):
		repo = Repo.clone_from(REPO_URL, path)
	else:
		repo = Repo(path)
	return repo

api.add_resource(Manager, '/')
api.add_resource(AddWorker, '/add_worker')

if __name__ == '__main__':
	num_workers_required = sys.argv[1]
	repo = get_repo("ManagerRepo")
	for commit in repo.iter_commits():
		commits_list.append(str(commit))
		commits_not_returned.append(str(commit))
		results_map[str(commit)] = -1
	print 'There are {0} commits'.format(len(commits_list))

	app.run(host='127.0.0.1', port=5000, debug=False)
