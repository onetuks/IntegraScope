# Overview
This project is an **AI-assisted development and operations support system** for SAP Integration Suite (IS, Cloud Integration).
It focuses on **FAILED test executions and message processing errors** to provide:

- Error analysis (highest priority)
- Root cause identification and solution guidance
- Knowledge accumulation via vector database
- Test automation (lower priority)

In current SAP EAI environments, error investigation heavily depends on individual experience.
Similar issues are repeatedly analyzed from scratch, and knowledge is rarely accumulated in a reusable form.

This system aims to automate the flow of  
**FAILED log → analysis → solution → knowledge reuse**,  
thereby reducing investigation time, minimizing trial-and-error, and accelerating decision-making.

Target users are SAP IS developers and EAI project leads.

---

# Core Features

## 1. FAILED Log Collection and Normalization (Toon)
- **What it does**  
  Collects FAILED message/test logs using the SAP IS Message Processing Log OData API and extracts only the fields required for analysis.
- **Why it matters**  
  Raw OData responses are large and noisy. Without standardized input, AI analysis and vector search quality degrade.
- **How it works**  
  - Fetch logs filtered by time range and optional iFlow ID
  - Extract error messages, adapter/communication type, error codes, and timestamps
  - Mask sensitive data and output a fixed JSON schema

---

## 2. AI-based Error Analysis and Solution Generation
- **What it does**  
  Analyzes normalized logs to classify error types, identify root causes, and propose concrete resolution steps.
- **Why it matters**  
  Developers need actionable guidance, not just summaries.
- **How it works**  
  - LangChain + LangGraph orchestrate the analysis flow
  - Gemini LLM generates results in a fixed, structured format
  - Clearly distinguishes evidence-based conclusions from assumptions

---

## 3. Similar Case Search and Knowledge Accumulation (Vector DB)
- **What it does**  
  Searches historical error cases and reuses proven solutions.
- **Why it matters**  
  Prevents repeated analysis of the same or similar issues and ensures consistency.
- **How it works**  
  - ChromaDB as the vector store
  - Hybrid search (dense embeddings + sparse keyword matching)
  - If similarity is low, a new analysis is generated and stored as a new case

---

## 4. Test Automation (Lower Priority)
- **What it does**  
  Executes SAP IS tests on demand and manages results.
- **Why it matters**  
  Connects test failures directly to error analysis in a single workflow.
- **How it works**  
  - Execute tests via SAP IS Test API
  - Display execution results
  - Automatically link FAILED tests to the analysis pipeline

---

# User Experience

## User Personas
- **IS Developer**  
  Needs fast and reliable error analysis during iFlow development and operations.
- **EAI Project Lead**  
  Oversees interface quality and aims to reduce recurring incidents.

## Key User Flows
1. User queries FAILED logs by time range or criteria
2. Selects a specific log entry and triggers analysis
3. System performs similarity search or AI-based analysis
4. User reviews structured root cause and solution guidance
5. (Optional) User executes tests and reviews results; failures link back to analysis

## UI/UX Considerations
- Streamlit-based simple and focused UI
- Markdown-based analysis output for readability
- Explicit display of confidence level and evidence

---

# Technical Architecture

## System Components
- FastAPI: Backend API
- LangChain / LangGraph: AI orchestration layer
- Gemini LLM: Error analysis and solution generation
- ChromaDB: Vector-based knowledge storage
- Streamlit: User interface

## Data Models
- **Case**
  - Normalized (toon) log summary
  - Error type, root causes, and solution steps
  - Metadata (iFlow, adapter, tags)
  - Embedding representation

## APIs and Integrations
- SAP IS Message Processing Log OData API
- SAP IS Test API
- Gemini LLM API

## Infrastructure Requirements
- Python 3.11+
- Docker-based local/server deployment
- Environment-variable-based secret management

---

# Development Roadmap

## Phase 1: MVP (Error Analysis First)
- MPL OData API integration
- Log normalization (toon)
- AI-based error analysis and solution generation
- Streamlit UI for results

## Phase 2: Knowledge Reuse
- ChromaDB integration
- Similar case search logic
- Persistent storage of analysis results

## Phase 3: Test Automation Expansion
- SAP IS Test API integration
- Test execution and result listing
- Seamless link between test failures and analysis

---

# Logical Dependency Chain

1. **Foundation**
   - Log collection and normalization
2. **Early Visible Frontend**
   - Streamlit-based log browsing and analysis view
3. **AI Analysis Stabilization**
   - Fixed output schema and prompt versioning
4. **Knowledge Accumulation**
   - Vector DB storage and retrieval
5. **Expansion**
   - Test automation features

---

# Risks and Mitigations

- **Log format variability**  
  → Incremental extension of normalization logic
- **LLM hallucination**  
  → Prioritize database-backed evidence and enforce clear labeling
- **Over-scoped MVP**  
  → Focus strictly on error analysis and solutions first

---

# Appendix

## Research / References
- SAP Integration Suite Message Processing Log OData API documentation
- LangChain / LangGraph orchestration patterns
- Hybrid vector search strategies (dense + sparse)
