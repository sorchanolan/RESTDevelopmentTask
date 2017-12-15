# RESTDevelopmentTask
Sorcha Nolan 13317836
REST development task in Python using the work-stealing method

This system can be run using the run.sh script, which takes one parameter - the number of worker nodes to be spun up.

## Manager.py
The manager must be set up first, and runs as a REST API. On setup, it clones the git repository (using https://github.com/parcel-bundler/parcel which has approx. 250 commits) and gets a list of the commit ids. It has three endpoints, two GET endpoints and one POST. The first GET endpoint receives requests from workers attempting to register with the manager. These are added until the number of workers is equal to the number of workers necessary according to the input parameter. From there, the workers send GET requests when they need another commit to process, and POST requests to return the processed data. When a commit has been returned with a value, this commit is removed from a list tracking commits returned. The system keeps sending out commits from this list until it is empty, so that if one of the nodes fails, another will take the same work and return it eventually. The time begins when all workers have been registered, and ends when the last commit is returned. 

## Worker.py
The worker nodes register with the manager to get their unique worker id, before cloning the repository. They then begin requesting work, being told to wait until all workers have been added. When all have been added, they repeatedly request work within a while loop until all commits have been sent out. When they get a commit, they execute the task by checking out the commit sent to them in the repo, then getting all files in each commit. The cyclomatic complexity is computed for each file, and the average is calculated then sent back to the manager, along with a request for another commit. 
