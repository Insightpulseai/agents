# Smoke Evaluation

## Purpose

Minimal evaluation to verify the published Agent Application responds correctly.

## Test cases

### 1. Informational

- Input: "What are the BIR filing deadlines for Q2 2026?"
- Expected: Response contains specific dates and form numbers
- Mode: PROD-ADVISORY

### 2. Navigational

- Input: "How do I run the SLSP report in Odoo?"
- Expected: Response contains navigation steps referencing Odoo menus
- Mode: PROD-ADVISORY

### 3. Compliance summary

- Input: "Show overdue compliance tasks."
- Expected: Response references task status and deadlines
- Mode: PROD-ADVISORY

### 4. Write block in advisory mode

- Input: "Create a compliance task for March VAT."
- Expected: Response explains that write actions require PROD-ACTION mode
- Mode: PROD-ADVISORY

### 5. Write with confirmation

- Input: "Create a compliance task for March VAT." (with confirmation=true)
- Expected: Response confirms task draft creation
- Mode: PROD-ACTION
