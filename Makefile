setup:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	cp .env.example .env

local-email-server:
	python -m smtpd -n -c DebuggingServer localhost:1025