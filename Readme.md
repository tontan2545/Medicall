# Medicall
Medicall is an IoT device which aids doctors in performing common diagnosis for patients. 

Our mission is to provide a low-cost, easy-to-use, and accurate device for patients to use in their daily practice.

# Setup
## Run setup script
This will do the following
- Generate and activate virtual env file
- Install required python packages
- Copy `.env.local` and rename to `.env`

```bash
make setup
```

## Run local mail server

This will run a local mail server on port 1025. When a mail is sent it'll be intercepted by the local mail server and will not be sent to real mail

```bash
make local-mail-server
```
