from flask_restful import Resource, Api
from flask import Flask

from cyclomatic_complexity import cyclo_complex 

NUM_WORKERS = 0
repo = "https://github.com/sorchanolan/RESTDevelopmentTask"

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

def main():
	print "Manager running"
	q = Queue()
	q.enqueue(cyclo_complex)

api.add_resource(Manager, '/')
api.add_resource(AddWorker, '/add_worker')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000, debug=False)
    #with Connection():
    #    main()
