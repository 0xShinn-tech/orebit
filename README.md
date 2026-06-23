🛸 Ore-Bit — Space Mining Fleet Management System

Welcome to Ore-Bit, a decentralized, full-stack application built to manage space mining fleets, track long-range sector scans, and log asteroid extraction operations in real time.

This project is built using a modern decoupled architecture: a robust Django REST Framework API handling the heavy lifting on the backend, and an interactive, data-driven Streamlit dashboard serving as the tactical frontend command center.
🚀 The Core Concept

Ore-Bit simulates a real-time telemetry and logistics hub for a deep-space mining corporation.

    The Backend acts as the central planetary database, enforcing strict validation on fleet vessel specs and logging every single ton of ore extracted across the cosmos.

    The Frontend connects to this API to visualize tactical data. It includes an interactive Space Radar that maps active asteroid signatures in real time, allowing operators to lock onto targets and instantly dispatch mining vessels.

🛠️ System Architecture & Directory Layout

The ecosystem runs on a decoupled client-server architecture, communicating entirely via JSON payloads over HTTP.
Plaintext

Ore-Bit/
│
├── manage.py                  # Django CLI management script
├── app.py                     # Streamlit Frontend application
│
├── orebit/                    # Django Core Configuration Directory
│   ├── settings.py            # Global app settings, CORS, and Middlewares
│   └── urls.py                # Global API routing & entry points
│
└── [your_app_name]/           # Core API Application Engine
    ├── models.py              # Database Schemas (Vessels, Logs, Radar Signals)
    ├── serializers.py         # Python-to-JSON Data Translators
    └── views.py               # Controller logic & open-access permissions

    Backend Engine (Port 8000): Built for high-availability telemetry intake. It operates under an Open Access policy (AllowAny) to ensure space vessels can stream extraction data without authentication friction.

    Command Center UI (Port 8501): A wide-layout, responsive analytical dashboard built with Streamlit. It features automated Graceful Degradation (Simulation Mode)—if the Django backend goes offline, the frontend intelligently falls back to simulated radar arrays and local cache mocks so the UI never crashes.

🎛️ Backend Blueprint (Django REST Framework)
Datamodels (models.py)
1. Nave (Fleet Vessel)

Tracks the active fleet ships patrolling and mining the sectors.

    nome (String, max 100): Unique vessel callsign.

    tipo (String, max 50): Ship class (Mineradora, Cargueiro, Reconhecimento).

    capacidade_maxima (Integer): Maximum cargo hold capacity in metric tons.

    velocidade_mineracao (Integer): Mining extraction speed rate, measured in tons per hour (t/h).

    status (String, max 50): Current operational state (Ativa, Em Manutenção, Inativa).

    quadrante (String, max 50): Current celestial deployment sector.

    data_registro (Date): Auto-generated timestamp when the ship joined the active fleet.

2. AlvoRadar (Radar Target)

Live anomalies and asteroid belts caught by long-range sensory arrays.

    nome_alvo (String, max 50): Asteroid/anomaly designation (e.g., Apophis-9).

    quadrante (String, max 20): Space sector where the ping originated.

    minerio_disponivel (String, max 50): Primary raw element scanned (e.g., Platinum, Iron).

    volume_estimado (Float): Total estimated mineral mass available for extraction.

    perigo_nivel (String, max 20): Environmental hazard rating (Baixo, Médio, Alto).

3. HistoricoExtraecoes (Extraction Log)

An immutable ledger containing chronological operation logs.

    nave (String, max 100): Callsign of the executing vessel.

    minerio (String, max 50): Type of element harvested.

    quantidade (Float): Exact volume extracted during the run.

    data (Date): Auto-stamped date of the mining entry.

REST API Endpoints

All API endpoints are structured under the /api/ prefix using the DRF DefaultRouter.
Method	Endpoint	Description	Expected JSON Payload
GET	/api/naves/	Fetches the entire active fleet	—
POST	/api/naves/	Integrates a new vessel into the database	{"nome": str, "tipo": str, "capacidade_maxima": int, "velocidade_mineracao": int, "status": str, "quadrante": str}
GET	/api/radar/	Streams live celestial scanner targets	—
GET	/api/historico/	Fetches the complete immutable mining ledger	—
POST	/api/historico/	Commits a successful extraction operation log	{"nave": str, "minerio": str, "quantidade": float}
📊 Frontend Command Center (Streamlit)

The UI leverages Streamlit's latest modern layout elements (width='stretch') paired with Plotly Express for premium data presentation.

    Central Dashboard (Analytics Hub): Displays real-time critical KPIs (total fleet capacity, monthly yields, mapped sectors) along with grouped interactive bar charts tracking mining outputs across different sectors.

    Space Radar (Tactical Array): Pulls raw tracking data from /api/radar/ to render an incredibly clean Polar Scatter Plot Chart. The size of each point dynamically reflects the asteroid's mineral mass, while colors reflect sector danger levels. Includes an integrated deployment form to instantly lock coordinates, select a ship, and hit "Extract".

    Fleet Logistics (Registration Form): A structured layout built to seamlessly feed telemetry into Django's exact strict validation constraints.

    Operations Log (Audit Ledger): Translates raw database logs into scannable dataframes for corporate record-keeping.

⚡ Quickstart Guide: Spinning Up Ore-Bit
1. Environment Setup

Make sure you have your virtual environment activated and your project dependencies installed:
Bash

pip install django djangorestframework django-cors-headers streamlit pandas plotly requests

2. Calibrate the Database (Backend)

Run your Django migrations to build the tables for your fleet, radar targets, and logs:
Bash

python manage.py makemigrations
python manage.py migrate

3. Launch the API Server

Start the backend server on its standard port (8000):
Bash

python manage.py runserver

4. Fire Up the Dashboard UI

Open a second terminal window (keep the virtual environment active) and launch your Streamlit engine:
Bash

streamlit run app.py

Your browser will pop open automatically at http://localhost:8501. Your fleet control deck is officially online!