setup: venv
	source $(PWD)/venv/bin/activate
	pip install -r requirements.txt
	cp .env.example .env

venv:
	python3 -m venv venv

local-email-server:
	python -m smtpd -n -c DebuggingServer localhost:1025

local-mqtt-server:
	mosquitto -v -c mosquitto.conf