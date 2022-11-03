# Medicall
Medicall is an IoT device which aids doctors in performing common diagnosis for patients. 

Our mission is to provide a low-cost, easy-to-use, and accurate device for patients to use in their daily practice.

---
## Setup
### Install python dependencies

```bash
pip install -r requitements.txt
```

### Generate env file

Copy `local.env` to `.env` and fill the corresponding values

### Run local mail server

This will run a local mail server on port 1025. When a mail is sent it'll be intercepted by the local mail server and will not be sent to real mail

```bash
make local-mail-server
```