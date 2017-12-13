#!/bin/sh

#pip install -r requirements.txt
python manager.py $1 &
for i in $( seq 1 $1 )
do
	python worker.py &
done