# EWDGroup8 – MoMo SMS Database Design & Data Processing System

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

> ⚠️ **Assessment Note:**
> Coding contributions are evidenced **strictly through GitHub commits** in database and schema-related files, as required by the grading policy.

---

## 📊 Scrum & Project Management

* Scrum board actively maintained and updated
* Week 1 tasks completed and Week 2 tasks tracked
* Clear ownership and sprint progression

🔗 **Scrum Board Link:** [Trello Link](https://trello.com/b/ayd4HWIa/enterprise-momo-data-system)

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



