
reset:
	rm -rf ~/.bushido-data

rmdb:
	rm -rf ~/.bushido-data/bushido.db

term:
	textual console -x EVENT -x SYSTEM -x DEBUG -x WORKER

run:
	textual run bushido/app.py --dev

