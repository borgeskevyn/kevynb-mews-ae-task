# MEWS

## Analytical Engineer

_Finance and Operations (Data)_

## Model Situation

We are rolling out a new infrastructure that consolidates general ledger (GL) data from multiple systems, including Salesforce (CRM) and Business Central (ERP). This includes journal entries, account metadata, entity hierarchies, and FX data.

Your stakeholder is our **Financial Planning & Analysis (FP&A) team**. Today they stitch numbers together manually across Salesforce and Business Central; they need a **trustworthy, single-reporting-currency (EUR) monthly view of the P&L** they can plan and report from. You are the analytics engineer building the reliable foundation they will depend on.

The data has already been ingested and surfaced into raw structured tables, and the environment is provided for you (see the Installation Guide below: Docker + PostgreSQL + a scaffolded dbt project). You do **not** need to set up infrastructure. You run it and build on top of it.

## Homework

You are working with a new general ledger dataset ingested from multiple systems. Your task is to design and build foundational dbt models that prepare this data for financial reporting and analytical integrity. The dataset includes journal entries, accounts, and entities.

Your stakeholder is the FP&A team (see above). To give a sense of where this ultimately leads, the kinds of questions they want to answer include monthly consolidated revenue in EUR by entity/territory, a simple P&L view (revenue vs expense over time), and confidence that the figures can be trusted. 

You do **not** need to deliver all of that.

### What We Expect:

- Use dbt to transform the data into a usable state for finance stakeholders.
- Focus on what you believe is core to enabling strong insights and building high trust in the data. You do not need to model everything.
- Apply rigorous testing to ensure data quality and control. Financial integrity is essential.

You are free to explore the data and design your models as you see fit. Prioritise clarity, consistency, and trust in the results. Please highlight any risks, challenges, or unexpected results you encounter and explain how they might be handled in production.

**We don't expect a finished, FP&A-ready deliverable in ~2 hours.** What matters is the quality of the foundations you build and your thinking. 

If you don't get all the way there (and you won't), clearly explain the next steps you'd take to reach a deliverable FP&A could actually use and the assumptions you have made.

### Using AI

We **encourage** you to use AI tools (Claude, Copilot, Cursor, etc.). Be aware though that we are **not** judging the AI's output: AI can almost certainly complete this assignment on its own. 
What we assess is **how you use it and your critical thinking**, your approach, the structure you choose, keeping the end users in mind, and turning data into insights and, above all, real value for the stakeholders and the business.

Please include a short written section in your submission describing: **which tools you used, where you used them, and what you checked or validated about their output and how.**

### Recorded Walkthrough

Prepare a **5–10 minute walkthrough** of your deliverable, **pitched to a non-data FP&A audience**. It's your choice how you deliver it:

- **Record it** — a screen recording using whatever tool you prefer (Loom, Zoom, QuickTime, etc.), shared as a link; or
- **Present it live** to us.

Either way, cover: the business question, what you built and why, a quick live look at the output, your key findings and any data-trust caveats, and how you used AI. We assess this for clarity and your ability to explain technical work to non-experts — not for production polish.

### Time Expectation:

Aim for roughly **2 hours of focused work** on the dbt project.

### Assessment Criteria:

- A **working dbt project**
- Modelling and testing rigour, and data integrity in a financial context
- Understanding of FP&A metrics and what the stakeholder actually needs
- **AI judgement**
- **Communication to a non-data audience**


Please submit the dbt project (zipped or as a GitHub repo) along with the above to the recruiter.


---

## Installation Guide

This project uses [uv](https://astral.sh/uv/) for fast, reliable Python dependency management and project setup.

### Prerequisites

- **Docker**: Required for PostgreSQL and API server containers
- **uv**: Required for Python dependency management and virtual environment setup

If you don't have `uv` installed, the build script will guide you through installation.

**Mac/Linux**

```sh
sh build.sh
```

**Windows**

```cmd
build.bat
```

The build script will:
1. ✅ Set up Docker containers (PostgreSQL database on port 5465, API server on port 3000)
2. ✅ Create a Python virtual environment with all dependencies
3. ✅ Run `dbt debug` to verify everything is working correctly

If you see `All checks passed!`, you're ready to go.

### Next Steps

Once the build completes successfully, activate the virtual environment and enter the dbt directory:

```sh
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate     # Windows

cd dbt
```

Alternatively, run commands without activating the venv:

```sh
uv run dbt run
uv run dbt test
```

## Cleanup Guide

**Mac/Linux**

```sh
sh clean.sh
```

**Windows**

```cmd
clean.bat
```

## Access Keys

- **Endpoint**: localhost:5465
- **Database Name**: proddb
- **Username**: produser
- **Password**: prodpassword
