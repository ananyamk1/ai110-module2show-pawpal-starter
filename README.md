# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Challenge 3: Advanced Priority Scheduling and UI
1. Time-based ordering with HH:MM task sorting (Scheduler.sort_by_time)
2. Flexible filtering by completion status and pet (Scheduler.filter_tasks)
3. Recurring task rollover for daily and weekly tasks when completed
4. Conflict warnings when multiple tasks share the same scheduled time
5. Next available slot search that scans merged busy intervals to find the earliest valid gap 


## Challenge 2: Agent Mode Data Persistence
1. Inspected the existing scheduler code and tests
2. Added a new interval-based algorithm (Scheduler.find_next_available_slot) that:-
Converts HH:MM values into minutes, Clips task intervals to a planning window, Merges overlaps
3. Added targeted tests to validate:-
Earliest-gap detection, Overlap merging behavior, No-gap scenarios returning None

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

Confidence Level:- (4/5)
