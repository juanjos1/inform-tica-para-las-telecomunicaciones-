# Centralized Routing Router Application

## Setup
Make sure the controller is running first, then:

```bash
cd centralized-routing-router
python -m app.main --id R1 --ip 127.0.0.1 --port 5001 --ctrl-host 127.0.0.1 --ctrl-port 9000
python -m app.main --id R2 --ip 127.0.0.1 --port 5002 --ctrl-host 127.0.0.1 --ctrl-port 9000
python -m app.main --id R3 --ip 127.0.0.1 --port 5003 --ctrl-host 127.0.0.1 --ctrl-port 9000
python -m app.main --id R4 --ip 127.0.0.1 --port 5004 --ctrl-host 127.0.0.1 --ctrl-port 9000
```

## Run tests
```bash
python -m pytest tests/ -v
```
