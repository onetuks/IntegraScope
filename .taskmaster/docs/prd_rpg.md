# PRD_RPG: SAP Integration Suite Test Automation Flow

## Overview
This document defines the **test automation flow (RPG-style step specification)** for SAP Integration Suite (IS) iFlow testing.
It focuses on **controlled, queue-based asynchronous execution** and seamless integration with **AI-driven error analysis and solution guidance**.

The goal is to make test execution **predictable, observable, and tightly coupled with failure analysis**, rather than a standalone automation feature.

---

## Test Automation Flow

### 1. iFlow List and Test Status Overview
- The system provides a list of available iFlows.
- Each row displays:
  - Artifact ID
  - Package name
  - Latest test execution status (SUCCESS / FAILED / NOT RUN)
  - Last execution timestamp
- Purpose:
  - Give users immediate visibility into test coverage and current quality state.

---

### 2. Enqueue iFlow for Testing
- The user selects one or more iFlows from the list.
- Selected iFlows are added to a **test waiting queue**.
- Each queue entry contains:
  - iFlow identifier
  - Requested execution time
  - Current queue status (WAITING / RUNNING / COMPLETED)
- Purpose:
  - Decouple user actions from immediate execution.
  - Enable controlled, sequential processing.

---

### 3. Manual Test Execution Trigger
- The user explicitly clicks the **“Run Tests”** button.
- No automatic execution occurs without user intent.
- Purpose:
  - Maintain human-in-the-loop control.
  - Prevent unintended load on SAP IS environments.

---

### 4. Asynchronous Queue-Based Test Execution
- Tests are executed asynchronously based on queue order.
- Concurrency control:
  - A maximum of **5 tests run in parallel**.
  - Additional queued tests remain in WAITING state until slots free up.
- Execution rules:
  - FIFO (First-In, First-Out) within the queue.
  - Each test execution is isolated.
- Purpose:
  - Protect SAP IS resources.
  - Ensure predictable execution behavior.

---

### 5. Test Result Collection and List Update
- Upon completion of each test:
  - Execution result (SUCCESS / FAILED)
  - Execution duration
  - Timestamp
- The iFlow list and test result view are updated in near real time.
- Purpose:
  - Provide immediate feedback.
  - Maintain a single source of truth for test outcomes.

---

### 6. Failure Handling and Error Analysis Integration
- If a test result is FAILED:
  - An **“Analyze Error”** button becomes available.
- On user action:
  - FAILED test logs are fetched via SAP IS Message Processing Log API.
  - Logs are normalized (toon).
  - AI-driven error analysis and solution derivation are executed.
- Output:
  - Error type classification
  - Root cause candidates
  - Troubleshooting checklist
  - Recommended fixes
- Purpose:
  - Turn test failures into actionable insights.
  - Eliminate manual log inspection loops.

---

## Design Principles
- Explicit user control over execution
- Deterministic queue behavior
- Bounded concurrency
- Tight coupling between test failure and analysis
- Observability over blind automation

---

## Non-Goals
- Automatic test execution on deploy
- Automatic iFlow modification or redeployment
- Real-time continuous monitoring

---

## Expected Outcome
- Developers can safely run multiple tests without overloading SAP IS.
- Failures immediately transition into structured analysis.
- Test automation becomes a gateway to faster problem resolution, not just execution.
