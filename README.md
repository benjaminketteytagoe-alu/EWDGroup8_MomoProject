# EWDGroup8_MomoProject

## The Momo Project Description
The Momo SMS is a full-stack mobile money solution designed to provide accessible financial services to users through USSD and SMS interfaces. Built with modern technologies(Frontend: HTML, CSS and JavaScript, Backend and Servers: flask, ngnix,RESTful-API, JSON file structure, CI/CD: git and Github) and following industry best practices, the platform enables users to perform a wide range of financial transactions. This project was carried out by [Team Members](## 👥 Team Members)


## Architecture Diagram

The project architecture diagram design can be accessed through this link: [Miro Architecture Board](https://miro.com/app/board/uXjVGS77-ss=/) 

**Project Structure**
```.
├── README.md                         # Setup, run, overview
├── .env.example                      # DATABASE_URL or path to SQLite
├── requirements.txt                  # lxml/ElementTree, dateutil, (FastAPI optional)
├── index.html                        # Dashboard entry (static)
├── web/
│   ├── styles.css                    # Dashboard styling
│   ├── chart_handler.js              # Fetch + render charts/tables
│   └── assets/                       # Images/icons (optional)
├── data/
│   ├── raw/                          # Provided XML input (git-ignored)
│   │   └── momo.xml
│   ├── processed/                    # Cleaned/derived outputs for frontend
│   │   └── dashboard.json            # Aggregates the dashboard reads
│   ├── db.sqlite3                    # SQLite DB file
│   └── logs/
│       ├── etl.log                   # Structured ETL logs
│       └── dead_letter/              # Unparsed/ignored XML snippets
├── etl/
│   ├── __init__.py
│   ├── config.py                     # File paths, thresholds, categories
│   ├── parse_xml.py                  # XML parsing (ElementTree/lxml)
│   ├── clean_normalize.py            # Amounts, dates, phone normalization
│   ├── categorize.py                 # Simple rules for transaction types
│   ├── load_db.py                    # Create tables + upsert to SQLite
│   └── run.py                        # CLI: parse -> clean -> categorize -> load -> export JSON
├── api/                              # Optional (bonus)
│   ├── __init__.py
│   ├── app.py                        # Minimal FastAPI with /transactions, /analytics
│   ├── db.py                         # SQLite connection helpers
│   └── schemas.py                    # Pydantic response models
├── scripts/
│   ├── run_etl.sh                    # python etl/run.py --xml data/raw/momo.xml
│   ├── export_json.sh                # Rebuild data/processed/dashboard.json
│   └── serve_frontend.sh             # python -m http.server 8000 (or Flask static)
└── tests/
    ├── test_parse_xml.py             # Small unit tests
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## 👥 Team Members

**Team Name:** EWDGroup 8
--------------------------------------------------------------------------------------------------------
|   Name  |                Role                     |              Primary Focus                       |
|---------|-----------------------------------------|--------------------------------------------------|
| Benjamin| Repo Manager/ Database/ Front(Back)end  | GitHub, ETL pipeline, Databases, Frontend/Backend|
| Eelaf   | Scrum Lead/ Backend/ Frontend           | Scrum board, server/backend, Frontend            |
| Peniel  | Scrum Assist/ Backend/ Database         | Scrum, Backend , server-side, database           |
| Alek    | Frontend/ Architecture/ Readme          | Dashboard, charts, ETL, Responsive design        |
| Prince  | Frontend/ Architecture/ Readme          | Dashboard, syst.Architecture, ETL, charts        |
--------------------------------------------------------------------------------------------------------

**NOTE:**
Since the project roadmap is structured into weeks, every team member works on every part of the project, depending on what we have for that week. This is to ensure even growth and understanding of the various parts of software development among our members. The roles are assigned to show who'll be leading us through each stage of the project.


## Project Management
[Trello Link](https://trello.com/invite/b/695fc3b3c63db147d018ef47/ATTI8ecd1b6d00c4415c80de14f330980be24B8DF08E/enterprise-momo-data-system)

**NOTE**
The project is still in its early stages, and we will continue to create and distribute tasks.
