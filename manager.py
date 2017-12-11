import os
from git import Repo
from flask_restful import Resource, Api
from flask import Flask

from cyclomatic_complexity import cyclo_complex 

NUM_WORKERS = 0
REPO_URL = "https://github.com/sorchanolan/RESTDevelopmentTask"
commits_list = []
repo = None

app = Flask(__name__)
api = Api(app)

class Manager(Resource):
	def post(self):  print "POST request"
	def get(self): return {"repo":repo}

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
