# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design focused on three core user actions: creating profiles for the owner and pet, managing care tasks, and generating a daily schedule that fits limited time as follows:-
1)Create Profiles/Accounts(Owner & Pet): Registree should input here their constraints of the day ("I only have 2 hours today") and the specific needs for their pet ("Cheetos is a energtic Golden Retriever")
2)Manage Tasks planned: Create, edit, prioritize specific activities like Morning Walk or Monthly Grooming with assigned importance: Essential vs. Optional or High Imp, Low Imp, etc
3)Generate Daily Schedule: Trigger a scheduling notification that selects the best tasks to fit within the registree's time window, prioritizing high-impact needs first
I included 4 classes:-
Pet -  Name, Species, energy levels, dietary needs, medical needs, other [Methods - update profile, get needs summary]
Tasks - description, duration, priority, category [Methods - edit task, get critical task]
Scheduler - time available, task list, add new tasks, get/generate plan [Methods - set daily limit, edit schedule]
Owner - Name, daily time available [Methods - add new task, generate plan, explain plan]


classDiagram
direction LR

class Owner {
  +name: String
  +dailyTimeAvailable: float
  +addNewTask(task: Task)
  +generatePlan(scheduler: Scheduler)
  +explainPlan()
}

class Pet {
  +name: String
  +species: String
  +energyLevel: String
  +dietaryNeeds: String
  +medicalNeeds: String
  +otherNotes: String
  +updateProfile()
  +getNeedsSummary(): String
}

class Task {
  +description: String
  +duration: int
  +priority: String
  +category: String
  +editTask()
  +getCriticalTask(): bool
}

class Scheduler {
  +timeAvailable: float
  +taskList: List~Task~
  +addNewTask(task: Task)
  +setDailyLimit(hours: float)
  +editSchedule()
  +generatePlan(owner: Owner, pets: List~Pet~): List~Task~
}

Owner "1" *-- "0..*" Pet : has
Owner "1" o-- "0..*" Task : manages
Owner "1" --> "1" Scheduler : uses
Scheduler "1" --> "0..*" Task : selects/prioritizes
Scheduler "1" ..> "0..*" Pet : considers needs

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yep, it changed during implementation, I added a pet_name to 'Task' since its connected to a particular pet in case owner has multiple pets; this can avoid scheduling decisions confusion. Also added add_pet method into Owner so that their relationship (Owner has Pets) is represented.
Then I linked Owner and Scheduler with Owner.tasks instance to avoid a logic bottleneck where Owner.tasks and Scheduler.task_list could drift out of sync possibly


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Contrainsts scheduler considered: time first and priority as top, then completed status. I chose to go with time and priority as the top most important because they directly affect whether the plan is both realistic and useful. A plan that ignores time is kinda impossible to follow, and a plan that ignores priority might miss the essential care tasks


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One key tradeoff is in conflict detection: I only check for exact HH:MM time matches instead of full overlapping durations (for example, 08:30-09:00 overlapping with 08:45-09:15). That means the system can miss some real conflicts, but it stays lightweight and easy to reason about.
This is reasonable for this scenario because PawPal needs fast, understandable warnings rather than heavy calendar-style logic. The simple check gives useful alerts without making the scheduling code too complex for this project scope.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used VS Code Copilot in multiple modes depending on the phase. In design mode, I used chat to pressure-test my class boundaries and method responsibilities before writing full logic. During implementation, I used Copilot to draft method scaffolds, edge-case checks, and cleaner function naming. In testing/debugging, I used Copilot to suggest test cases, diagnose import issues, and validate whether failures came from test assumptions or scheduler behavior.

The most helpful prompts were specific and constraint-based, for example: "Given this scheduler rule, what are the highest-risk edge cases?" and "Does this method introduce coupling between Owner and Scheduler?" Prompts that included expected behavior, not just code requests, gave the best results.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One example was when AI suggested a more compact, Pythonic refactor of my conflict-detection method (using `defaultdict` and tighter inline expressions). I reviewed it, compared it with my current version, and decided not to adopt it fully because my explicit step-by-step version was easier to read and explain for this project. I verified that decision by running my tests and terminal demo to confirm the current method still produced correct conflict warnings and kept the logic easy to follow.

Another case was with architecture suggestions that mixed storage ownership between `Owner` and `Scheduler`. I modified that suggestion to keep the source of truth with pet-attached tasks and let `Scheduler` compute plans from owner data. I verified this by checking method responsibilities (`get_all_tasks`, `retrieve_tasks_from_owner`, `generate_plan`) and rerunning tests after each change.

**c. Prompt Comparison (Two-Model Evaluation)**

I compared two model answers for weekly task rescheduling.

Prompt I used:
"Design a simple, modular Python solution to reschedule weekly pet tasks after completion."

- Model 1: GPT-5.3-Codex (OpenAI)
- Model 2: Claude (Anthropic)

I found GPT-5.3-Codex better for my codebase.

- It split the logic into cleaner steps.
- It kept `Owner` and `Scheduler` roles clear.
- It was easier for me to test and read.

Claude's answer worked, but it had more branching in one place and felt less clean.

So I chose the GPT-5.3-Codex style because it felt more modular and more Pythonic in my project.

Separate chat sessions for each project phase helped me stay organized because each thread had a single objective: design/UML, implementation, testing, and packaging. This reduced context drift, made prompts more precise, and made it easier to audit decisions when writing this reflection.

The biggest lesson about being the lead architect is that AI is strongest as a fast design and coding collaborator, but I still own system coherence. I had to define constraints, reject over-complicated suggestions, and enforce consistency between UML, code, tests, and UI. The final quality came from human judgment plus AI acceleration, not from accepting suggestions blindly.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested core scheduler behaviors that directly affect correctness and trust:

- Chronological sorting behavior (`sort_by_time`) so users see tasks in expected order.
- Recurrence logic for completed daily and weekly tasks so ongoing care tasks continue automatically.
- Conflict detection for duplicate HH:MM times so owners get warnings when schedules clash.
- Basic task lifecycle checks such as marking complete and adding tasks to a pet.

These tests were important because they cover the central algorithmic contract of the app: selecting, ordering, and maintaining tasks safely across days.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
My confidence level is **4/5**. The current suite validates the most important scheduling rules and passed consistently with `python -m pytest`.

If I had more time, I would add edge-case tests for:

- A pet with zero tasks.
- Multiple tasks sharing the same timestamp for one pet vs across pets.
- Invalid time strings and malformed input combinations.
- Boundary time budgets (exact-fit minutes vs one-minute overflow).
- Overlapping-duration conflicts (not just exact same start times).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with how the algorithmic layer stayed clean while still becoming meaningfully smarter. I added sorting, filtering, recurrence, and conflict warnings without turning the project into an over-engineered calendar system.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
In the next iteration, I would improve conflict handling from exact-time detection to duration-overlap detection and add in-UI conflict resolution helpers (for example, quick edit controls for conflicting task times). I would also expand test coverage around negative/invalid inputs and long-term recurrence behavior.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
My key takeaway is that strong AI collaboration depends on clear architectural intent. When I treated Copilot as a junior pair programmer and kept myself in the lead architect role, I got faster implementation without sacrificing design clarity or system reliability.

## 📸 Demo

<a href="/course_images/ai110/pawpal_home.png" target="_blank"><img src='/course_images/ai110/pawpal_home.png' title='PawPal App - Home' width='' alt='PawPal App - Home' class='center-block' /></a>

<a href="/course_images/ai110/pawpal_owner_setup.png" target="_blank"><img src='/course_images/ai110/pawpal_owner_setup.png' title='PawPal App - Owner Setup' width='' alt='PawPal App - Owner Setup' class='center-block' /></a>

<a href="/course_images/ai110/pawpal_task_form.png" target="_blank"><img src='/course_images/ai110/pawpal_task_form.png' title='PawPal App - Task Form' width='' alt='PawPal App - Task Form' class='center-block' /></a>

<a href="/course_images/ai110/pawpal_task_insights.png" target="_blank"><img src='/course_images/ai110/pawpal_task_insights.png' title='PawPal App - Task Insights' width='' alt='PawPal App - Task Insights' class='center-block' /></a>

<a href="/course_images/ai110/pawpal_schedule_plan.png" target="_blank"><img src='/course_images/ai110/pawpal_schedule_plan.png' title='PawPal App - Generated Plan' width='' alt='PawPal App - Generated Plan' class='center-block' /></a>

<a href="/course_images/ai110/pawpal_uml_final.png" target="_blank"><img src='/course_images/ai110/pawpal_uml_final.png' title='PawPal UML Final Diagram' width='' alt='PawPal UML Final Diagram' class='center-block' /></a>
















classDiagram
direction LR

class Owner {
  +name: str
  +daily_time_available: float
  +pets: List~Pet~
  +scheduler: Scheduler
  +add_pet(pet: Pet)
  +get_pet(pet_name: str) Pet
  +add_new_task(task: Task, pet_name: Optional~str~)
  +get_all_tasks(include_completed: bool) List~Task~
  +generate_plan() List~Task~
  +mark_task_complete(task: Task) Optional~Task~
  +explain_plan() str
}

class Pet {
  +name: str
  +species: str
  +energy_level: str
  +dietary_needs: str
  +medical_needs: str
  +other_notes: str
  +tasks: List~Task~
  +update_profile(...)
  +get_needs_summary() str
  +add_task(task: Task)
  +get_tasks(include_completed: bool) List~Task~
}

class Task {
  +description: str
  +duration: int
  +time: Optional~str~
  +due_date: Optional~date~
  +frequency: str
  +completed: bool
  +priority: str
  +category: str
  +pet_name: Optional~str~
  +edit_task(...)
  +get_critical_task() bool
  +mark_complete()
  +mark_incomplete()
  +is_valid_time_format(time_value: str) bool
}

class Scheduler {
  +time_available: float
  +task_list: List~Task~
  +last_plan: List~Task~
  +last_warnings: List~str~
  +add_new_task(task: Task)
  +set_daily_limit(hours: float)
  +edit_schedule(tasks: List~Task~)
  +retrieve_tasks_from_owner(owner: Owner, include_completed: bool) List~Task~
  +organize_tasks(tasks: List~Task~) List~Task~
  +sort_by_time(tasks: List~Task~) List~Task~
  +filter_tasks(tasks: List~Task~, completed: Optional~bool~, pet_name: Optional~str~) List~Task~
  +mark_task_complete(owner: Owner, task: Task) Optional~Task~
  +detect_time_conflicts(tasks: List~Task~) List~str~
  +generate_plan(owner: Owner) List~Task~
}

Owner "1" *-- "0..*" Pet : has
Pet "1" *-- "0..*" Task : owns
Owner "1" --> "1" Scheduler : uses
Scheduler ..> Owner : reads tasks
Scheduler ..> Task : sorts/filters/plans