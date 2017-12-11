import os
from git import Repo
from flask_restful import Resource, Api
from flask import Flask

from cyclomatic_complexity import cyclo_complex 

NUM_WORKERS = 0
REPO_URL = "https://github.com/sorchanolan/RESTDevelopmentTask"
commits_list = []
commits_index = 0
repo = None
finished = False

app = Flask(__name__)
api = Api(app)

class Manager(Resource):

	def get(self): 
		global commits_list, commits_index, finished

		if commits_index < len(commits_list):
			commit = commits_list[commits_index]
			commits_index += 1
		else:
			commit = None
			finished = True
		return {"commit": commit, "finished": finished}


	def post(self):  print "POST request"

class AddWorker(Resource):
	def get(self): 
		global NUM_WORKERS
		response = {"new_worker":NUM_WORKERS}
		print "New worked added: {0}".format(NUM_WORKERS)
		NUM_WORKERS += 1
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
	repo = get_repo("RepoFolder")
	for commit in repo.iter_commits():
		commits_list.append(str(commit))
	print 'There are {0} commits'.format(len(commits_list))

	app.run(host='127.0.0.1', port=5000, debug=False)
