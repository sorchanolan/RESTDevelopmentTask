from rq import Connection, Queue

from cyclomatic_complexity import cyclo_complex 

def main():
	print "Manager running"
	q = Queue()
	q.enqueue(cyclo_complex)


if __name__ == '__main__':
    with Connection():
        main()

