from dataclasses import dataclass, field
from datetime import date, timedelta
import re
from typing import List, Optional


@dataclass
class Pet:
    name: str
    species: str
    energy_level: str
    dietary_needs: str
    medical_needs: str
    other_notes: str = ""
    tasks: List["Task"] = field(default_factory=list)

    def update_profile(
        self,
        energy_level: Optional[str] = None,
        dietary_needs: Optional[str] = None,
        medical_needs: Optional[str] = None,
        other_notes: Optional[str] = None,
    ) -> None:
        """Update one or more mutable profile fields for this pet."""
        if energy_level is not None:
            self.energy_level = energy_level
        if dietary_needs is not None:
            self.dietary_needs = dietary_needs
        if medical_needs is not None:
            self.medical_needs = medical_needs
        if other_notes is not None:
            self.other_notes = other_notes

    def get_needs_summary(self) -> str:
        """Return a compact summary of this pet's core care needs."""
        return (
            f"{self.name} ({self.species}) | "
            f"Energy: {self.energy_level} | "
            f"Diet: {self.dietary_needs} | "
            f"Medical: {self.medical_needs}"
        )

    def add_task(self, task: "Task") -> None:
        """Attach a task to this pet and set task ownership metadata."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self, include_completed: bool = True) -> List["Task"]:
        """Return this pet's tasks, optionally filtering out completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]


@dataclass
class Task:
    description: str
    duration: int
    time: Optional[str] = None
    due_date: Optional[date] = None
    frequency: str = "daily"
    completed: bool = False
    priority: str = "medium"
    category: str = "general"
    pet_name: Optional[str] = None

    def edit_task(
        self,
        description: Optional[str] = None,
        duration: Optional[int] = None,
        time: Optional[str] = None,
        due_date: Optional[date] = None,
        frequency: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> None:
        """Update one or more task fields with basic validation."""
        if description is not None:
            self.description = description
        if duration is not None:
            if duration <= 0:
                raise ValueError("Task duration must be greater than 0.")
            self.duration = duration
        if time is not None:
            if not Task.is_valid_time_format(time):
                raise ValueError("Task time must use HH:MM 24-hour format.")
            self.time = time
        if due_date is not None:
            self.due_date = due_date
        if frequency is not None:
            self.frequency = frequency
        if priority is not None:
            self.priority = priority
        if category is not None:
            self.category = category
        if completed is not None:
            self.completed = completed

    def get_critical_task(self) -> bool:
        """Return True when this task should be treated as high priority."""
        return self.priority.strip().lower() == "high"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    @staticmethod
    def is_valid_time_format(time_value: str) -> bool:
        """Return True when time string matches HH:MM in 24-hour format."""
        if not re.fullmatch(r"\d{2}:\d{2}", time_value):
            return False
        hours, minutes = time_value.split(":")
        return 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59


class Scheduler:
    def __init__(self, time_available: float) -> None:
        """Initialize scheduler state with the owner's daily time budget."""
        self.time_available = time_available
        self.task_list: List[Task] = []
        self.last_plan: List[Task] = []
        self.last_warnings: List[str] = []

    def add_new_task(self, task: Task) -> None:
        """Add a task to the scheduler's internal task collection."""
        self.task_list.append(task)

    def set_daily_limit(self, hours: float) -> None:
        """Set the maximum available scheduling time for the day."""
        if hours <= 0:
            raise ValueError("Daily limit must be greater than 0.")
        self.time_available = hours

    def edit_schedule(self, tasks: List[Task]) -> None:
        """Replace the scheduler's current task collection."""
        self.task_list = list(tasks)

    def retrieve_tasks_from_owner(self, owner: "Owner", include_completed: bool = False) -> List[Task]:
        """Fetch tasks from an owner across all pets."""
        return owner.get_all_tasks(include_completed=include_completed)

    def organize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority and then by shorter duration first."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        def sort_key(task: Task) -> tuple:
            priority_rank = priority_order.get(task.priority.strip().lower(), 3)
            return (priority_rank, task.duration)

        return sorted(tasks, key=sort_key)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by HH:MM start time, then untimed tasks last.

        This method expects `Task.time` values to be normalized as `HH:MM` in
        24-hour format. Timed tasks are sorted lexicographically, which is
        valid for zero-padded time strings.
        """
        return sorted(
            tasks,
            key=lambda task: (
                task.time is None,
                task.time if task.time is not None else "99:99",
            ),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or assigned pet.

        Args:
            tasks: Candidate tasks to filter.
            completed: When provided, keep only tasks whose completed flag
                matches this value.
            pet_name: When provided, keep only tasks assigned to this pet.
        """
        filtered_tasks = list(tasks)
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed == completed]
        if pet_name is not None:
            filtered_tasks = [task for task in filtered_tasks if task.pet_name == pet_name]
        return filtered_tasks

    def mark_task_complete(self, owner: "Owner", task: Task) -> Optional[Task]:
        """Mark a task complete and spawn the next recurring instance when needed.

        Daily tasks create a new task due tomorrow. Weekly tasks create a new
        task due in seven days. Non-recurring frequencies are only marked
        complete and return None.
        """
        task.mark_complete()

        frequency_value = task.frequency.strip().lower()
        recurrence_days = {"daily": 1, "weekly": 7}
        if frequency_value not in recurrence_days:
            return None

        next_due_date = date.today() + timedelta(days=recurrence_days[frequency_value])
        next_task = Task(
            description=task.description,
            duration=task.duration,
            time=task.time,
            due_date=next_due_date,
            frequency=task.frequency,
            completed=False,
            priority=task.priority,
            category=task.category,
            pet_name=task.pet_name,
        )

        if task.pet_name:
            owner.add_new_task(next_task, pet_name=task.pet_name)
        else:
            self.add_new_task(next_task)

        return next_task

    def detect_time_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return lightweight warning strings for same-time task conflicts.

        This intentionally checks exact HH:MM matches only, which keeps runtime
        and logic simple for daily planning. It does not compute overlapping
        duration windows.
        """
        tasks_by_time: dict[str, List[Task]] = {}
        for task in tasks:
            if task.time is None:
                continue
            tasks_by_time.setdefault(task.time, []).append(task)

        warnings: List[str] = []
        for time_slot, slot_tasks in sorted(tasks_by_time.items()):
            if len(slot_tasks) < 2:
                continue

            pet_names = sorted({task.pet_name or "Unassigned" for task in slot_tasks})
            task_labels = [f"{task.description} ({task.pet_name or 'Unassigned'})" for task in slot_tasks]
            if len(pet_names) == 1:
                warning = (
                    f"Warning: {len(slot_tasks)} tasks for {pet_names[0]} are scheduled at {time_slot}: "
                    + ", ".join(task_labels)
                )
            else:
                warning = (
                    f"Warning: {len(slot_tasks)} tasks across pets are scheduled at {time_slot}: "
                    + ", ".join(task_labels)
                )
            warnings.append(warning)

        self.last_warnings = warnings
        return warnings

    def generate_plan(self, owner: "Owner") -> List[Task]:
        """Build a daily task plan that fits within the available minutes."""
        available_minutes = int(self.time_available * 60)
        candidate_tasks = self.retrieve_tasks_from_owner(owner, include_completed=False)
        self.detect_time_conflicts(candidate_tasks)
        ordered_tasks = self.organize_tasks(candidate_tasks)

        planned: List[Task] = []
        used_minutes = 0
        for task in ordered_tasks:
            if used_minutes + task.duration <= available_minutes:
                planned.append(task)
                used_minutes += task.duration

        self.last_plan = planned
        return planned


class Owner:
    def __init__(self, name: str, daily_time_available: float) -> None:
        """Create an owner with pet collection and an attached scheduler."""
        self.name = name
        self.daily_time_available = daily_time_available
        self.pets: List[Pet] = []
        self.scheduler = Scheduler(daily_time_available)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet for this owner, preventing duplicates by name."""
        if any(existing_pet.name == pet.name for existing_pet in self.pets):
            raise ValueError(f"Pet '{pet.name}' already exists for this owner.")
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Pet:
        """Return a pet by name or raise an error when not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        raise ValueError(f"No pet found with name '{pet_name}'.")

    def add_new_task(self, task: Task, pet_name: Optional[str] = None) -> None:
        """Assign a new task to one of the owner's pets."""
        target_pet_name = pet_name or task.pet_name
        if not target_pet_name:
            raise ValueError("Task must be assigned to a pet using pet_name.")

        pet = self.get_pet(target_pet_name)
        pet.add_task(task)

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Aggregate tasks from all pets, with optional completion filtering."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks(include_completed=include_completed))
        return all_tasks

    def generate_plan(self) -> List[Task]:
        """Generate and return today's plan using this owner's scheduler."""
        self.scheduler.set_daily_limit(self.daily_time_available)
        return self.scheduler.generate_plan(self)

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task and create the next recurring instance when applicable."""
        return self.scheduler.mark_task_complete(self, task)

    def explain_plan(self) -> str:
        """Return a readable text explanation of the most recent plan."""
        if not self.scheduler.last_plan:
            return "No plan generated yet."

        plan_lines = [
            f"Daily plan for {self.name} ({self.daily_time_available:.1f}h available):"
        ]
        for index, task in enumerate(self.scheduler.last_plan, start=1):
            pet_label = task.pet_name if task.pet_name else "Unassigned"
            plan_lines.append(
                f"{index}. {task.description} ({task.duration} min, {task.priority} priority) for {pet_label}"
            )

        total_minutes = sum(task.duration for task in self.scheduler.last_plan)
        plan_lines.append(f"Total scheduled time: {total_minutes} minutes")
        return "\n".join(plan_lines)
