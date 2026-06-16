# Centralized Routing System
**Course:** Informatics for Telecommunications | **Team:** The Developers

## Quick Start

### 1. Start the Controller (Terminal 1)
```bash
cd centralized-routing-controller
python -m app.main --protocol tcp --host 127.0.0.1 --port 9000
```

### 2. Start Router instances (separate terminals)
```bash
cd centralized-routing-router
python -m app.main --id R1 --ip 127.0.0.1 --port 5001 --ctrl-host 127.0.0.1 --ctrl-port 9000
python -m app.main --id R2 --ip 127.0.0.1 --port 5002 --ctrl-host 127.0.0.1 --ctrl-port 9000
python -m app.main --id R3 --ip 127.0.0.1 --port 5003 --ctrl-host 127.0.0.1 --ctrl-port 9000
python -m app.main --id R4 --ip 127.0.0.1 --port 5004 --ctrl-host 127.0.0.1 --ctrl-port 9000
```

### 3. Typical Router workflow (via menu)
1. Select **1** → Register with controller
2. Select **2** → Add neighbors (repeat for each neighbor)
3. Select **3** → Send topology (receives routing table back)
4. Select **4** → Show routing table (`show routing-table`)
5. Select **6** → Simulate link cost change

### 4. Run tests
```bash
cd centralized-routing-controller && python -m pytest tests/ -v
cd centralized-routing-router     && python -m pytest tests/ -v
```

## Requirements covered
FR-01 Router registration | FR-02 Neighbor info | FR-03 Topology storage
FR-04 Dijkstra shortest path | FR-05 Routing table generation | FR-06 Table delivery
FR-07 CLI display | FR-08 Link cost update | FR-09 Event logging
NFR-01..NFR-08 all satisfied (Python, modular, CLI, JSON, error handling, scalable, documented, tested)
