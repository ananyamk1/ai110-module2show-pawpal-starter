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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One example was when AI suggested a more compact, Pythonic refactor of my conflict-detection method (using `defaultdict` and tighter inline expressions). I reviewed it, compared it with my current version, and decided not to adopt it fully because my explicit step-by-step version was easier to read and explain for this project. I verified that decision by running my tests and terminal demo to confirm the current method still produced correct conflict warnings and kept the logic easy to follow.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
