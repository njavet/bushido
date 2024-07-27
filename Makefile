
reset:
	rm -rf ~/.bushido-data

rmdb:
	rm -rf ~/.bushido-data/bushido.db

term:
	textual console -x EVENT -x SYSTEM -x DEBUG -x WORKER

run:
	export PYTHONPATH=${PYTHONPATH}:'.'
	textual run bushido/app.py --dev

