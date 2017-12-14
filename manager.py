import os, sys, time

from git import Repo
from flask_restful import Resource, Api
from flask import Flask, request
from random import randint

NUM_WORKERS = 0
REPO_URL = "https://github.com/parcel-bundler/parcel"
commits_list = []
commits_not_returned = []
commits_index = 0
repo = None
finished = False
results_list = []
results_map = dict()
start_time = 0.0
end_time = 0.0

app = Flask(__name__)
api = Api(app)

class Manager(Resource):

	def get(self): 
		global commits_list, commits_index, finished, start_time

		if NUM_WORKERS == int(num_workers_required):
			if commits_index == 0:
				start_time = time.time()
			if commits_index < len(commits_list):
				print "Sending out commit {0}".format(commits_index)
				commit = commits_list[commits_index]
				commits_index += 1
			elif commits_index == len(commits_list) - 1:
				print "Commits sent out, {0} not returned".format(len(commits_not_returned))
				if len(commits_not_returned) > 0:
					commit = commits_list[randint(0, len(commits_not_returned) - 1)]
			else:
				commit = None
				finished = True
		else:
			commit = "wait"
			print "Waiting, {0} workers out of {1}".format(NUM_WORKERS, num_workers_required)

		return {"commit": commit, "finished": finished}


	def post(self):
		response = request.get_json()
		results_list.append(response['average_complexity'])
		commits_not_returned.remove(response['commit'])
		results_map[response['commit']] = response['average_complexity']
		print "{0} of {1} returned by {2}".format(response['average_complexity'], response['commit'], response['worker_id'])
		if len(commits_not_returned) == 0:
			end_time = time.time()
			print "Finished - {0} workers taking {1} seconds".format(num_workers_required, str(end_time - start_time))
			print "Average cyclomatic complexity for repo is {0}".format(get_average_cyclo_complex())
			finished()


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

def finished():
	global end_time
		
	# func = request.environ.get('werkzeug.server.shutdown')
	# if func is None:
	# 	raise RuntimeError('Not running with the Werkzeug Server')
	# func()

def get_average_cyclo_complex():
	global results_map
	sum = 0
	for key, value in results_map.iteritems():
		sum += value
	if len(results_map) != 0:
		return sum / len(results_map)
	return 0 

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
