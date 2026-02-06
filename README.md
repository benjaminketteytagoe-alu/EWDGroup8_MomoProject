# EWDGroup8 – MoMo SMS Database Design & Data Processing System

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Learning Objectives Alignment](#-learning-objectives-alignment)
3. [Entity Relationship Diagram (ERD)](#-entity-relationship-diagram-erd)
   - [Core Entities Implemented](#core-entities-implemented)
   - [ERD Design Highlights](#erd-design-highlights)
   - [Overall Project Architecture](#overall-project-architecture)
4. [SQL Database Implementation (MySQL)](#sql-database-implementation-mysql)
   - [Database Features](#database-features)
   - [Implementation File](#implementation-file)
   - [SQL Components Included](#sql-components-included)
5. [JSON Data Modeling & Serialization](#-json-data-modeling--serialization)
   - [Included JSON Examples](#included-json-examples)
   - [Key Strengths](#key-strengths)
6. [Repository Structure](#-repository-structure-rubric-aligned)
7. [Team Collaboration & Contributions](#-team-collaboration--contributions)
8. [Scrum & Project Management](#-scrum--project-management)
9. [Database Design Document (PDF)](#-database-design-document-pdf)
10. [AI Usage Policy Compliance](#-ai-usage-policy-compliance)
11. [License](#-license)

---

## 📌 Project Overview

The **MoMo SMS Database Design Project** focuses on designing and implementing a **robust, scalable relational database** for processing Mobile Money (MoMo) transaction data extracted from SMS/XML records. This phase emphasizes **database modeling, integrity enforcement, structured serialization, and collaborative engineering practices**.

The system is designed to support:

* Accurate storage of MoMo transaction data
* Efficient querying and analysis
* Secure, auditable ETL processing
* Future API-based data consumption via JSON serialization

This repository represents **Week 2 deliverables**, building upon the team setup established in Week 1.

---

## 🎯 Learning Objectives Alignment

This project explicitly addresses the following learning outcomes:

* Entity Relationship Diagram (ERD) Design
* SQL Database Implementation (MySQL)
* JSON Data Modeling & Serialization
* Team Collaboration & Professional Documentation
* Responsible and Transparent AI Usage

---

## 🧩 Entity Relationship Diagram (ERD)

### Core Entities Implemented

* **Transactions** – Main transaction records
* **Users** – Senders and receivers
* **Transaction_Categories** – Payment/transfer types
* **System_Logs** – ETL and processing audit logs
* **Transaction_Users (Junction Table)** – Resolves many-to-many relationships

### ERD Design Highlights

* Clear entity identification and naming
* Complete attribute lists with appropriate MySQL data types
* Explicit **Primary Keys (PK)** and **Foreign Keys (FK)**
* Accurate relationship cardinality (1:1, 1:M, M:N)
* Proper resolution of M:N relationships via junction tables
* Designed using a professional diagramming tool (Draw.io)

### Overall Project Architecture
**EWDGroup8_MomoProject** - [Miro link](https://miro.com/app/live-embed/uXjVGS77-ss=/?embedMode=view_only_without_ui&moveToViewport=-2336%2C-962%2C9027%2C5263&embedId=871724349883)

📁 **Location:**

```
docs/erd_diagram.png
```

📄 **Design Rationale:**
A **250–300+ word justification** explaining normalization decisions, integrity enforcement, and scalability considerations is included in the Database Design Document.

---

## 🗄️ SQL Database Implementation (MySQL)

### Database Features

* Fully normalized relational schema
* Strong referential integrity using `FOREIGN KEY` constraints
* `CHECK` constraints to ensure data accuracy
* Strategic indexing for performance optimization
* Meaningful column comments for documentation
* Realistic test data (5+ records per main table)

### Implementation File

```
database/database_setup.sql
```

### SQL Components Included

* DDL statements (`CREATE TABLE`, constraints, indexes)
* DML statements (`INSERT` test data)
* Tested CRUD operations (CREATE, READ, UPDATE, DELETE)

📸 Screenshots of executed queries and results are included in the Database Design PDF.

---

## 🔄 JSON Data Modeling & Serialization

JSON schemas were designed to represent how relational data is serialized for API consumption.

### Included JSON Examples

* Users
* Transactions
* Transaction Categories
* System Logs
* **Complex nested transaction object** including:

  * Sender and receiver details
  * Transaction category
  * Amount, timestamp, status
  * Processing metadata

### Key Strengths

* Proper nesting for related entities
* Accurate data types and realistic API response formats
* Clear mapping between SQL tables and JSON structures

📁 **Location:**

```
examples/json_schemas.json
```

---

## 📂 Repository Structure (Rubric-Aligned)

```
├── README.md
├── docs/
│   ├── erd_diagram.png
│   └── database_design.pdf
├── database/
│   └── database_setup.sql
├── examples/
│   └── json_schemas.json
├── data/
│   └── sample_queries.sql
├── scrum/
│   └── scrum_board_link.txt
└── ai-usage/
    └── ai_usage_log.md
```

---

## 👥 Team Collaboration & Contributions

**Team Name:** EWDGroup 8

| Name         | Role                               | Week 2 Responsibilities                                                                                         |
| ------------ | ---------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Benjamin** | Repository Manager / Database Lead | ERD design, schema definition, MySQL implementation, constraints, indexing, sample queries, GitHub coordination |
| **Peniel**   | Backend / Database Support         | ERD validation, SQL constraint review, data dictionary support, test data validation                            |
| **Eelaf**    | Scrum Lead / Backend               | Sprint planning, Scrum board management, task tracking, delivery coordination                                   |
| **Alek**     | Architecture / Documentation       | ERD consistency checks, JSON modeling support, documentation structure                                          |
| **Prince**   | Architecture / Documentation       | SQL-to-JSON mapping review, documentation refinement, architecture alignment                                    |



---

## 📊 Scrum & Project Management

* Scrum board actively maintained and updated
* Week 1 tasks completed and Week 2 tasks tracked
* Clear ownership and sprint progression

🔗 **Scrum Board Link:** [Trello Link](https://trello.com/b/ayd4HWIa/enterprise-momo-data-system)
---
**Database set-up - Team task sheet:** [Team Sheet Week 1](https://docs.google.com/spreadsheets/d/1pLqAZHWq_aOthOz3-OGXTW5T2kNAta_HwkuL4k555s4/edit?usp=sharing)
---
---
**REST API set-up - Team task sheet:** [Team Sheet Week 2](https://docs.google.com/spreadsheets/d/1-vjkeSLSdbb2df2L4AW_BbHfsWWAAuI2fukOLLNA-_o/edit?usp=sharing)
---

## 📄 Database Design Document (PDF)

The submitted PDF includes:

* ERD with annotations
* Detailed design rationale
* Data dictionary (tables & columns)
* Sample CRUD and analytical queries
* Query execution screenshots
* Security and data accuracy rules
* Professional formatting and layout

📁 **Location:**

```
docs/database_design.pdf
```

---

## 🤖 AI Usage Policy Compliance

* AI usage strictly limited to:

  * Grammar and formatting checks
  * SQL syntax verification
  * MySQL best-practice research (cited)
* No AI-generated ERD, schema logic, or business rules


---

## 📜 License

This project is licensed under the **MIT License**.
