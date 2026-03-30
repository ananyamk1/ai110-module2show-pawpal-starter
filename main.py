from pawpal_system import Owner, Pet, Task
try:
    from tabulate import tabulate
except ModuleNotFoundError:  # pragma: no cover - exercised in runtime-only CLI flow
    tabulate = None


PRIORITY_BADGES = {
    "high": "🔴 High",
    "medium": "🟠 Medium",
    "low": "🟡 Low",
}

STATUS_BADGES = {
    True: "✅ Done",
    False: "🔷 Pending",
}

TASK_TYPE_EMOJIS = {
    "feeding": "🍽️",
    "exercise": "🐾",
    "medical": "💊",
    "grooming": "🛁",
    "training": "🎯",
    "enrichment": "🧩",
    "general": "📌",
}


def task_type_label(task: Task) -> str:
    category = task.category.strip().lower()
    return f"{TASK_TYPE_EMOJIS.get(category, '📌')} {category.title()}"


def print_section(title: str) -> None:
    print(f"\n{title}")
    print("-" * 80)


def render_table(rows: list[list[object]], headers: list[str]) -> str:
    """Render table with tabulate when available, else plain aligned columns."""
    if tabulate is not None:
        return tabulate(rows, headers=headers, tablefmt="rounded_outline")

    string_rows = [[str(cell) for cell in row] for row in rows]
    widths = [len(header) for header in headers]
    for row in string_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def format_row(columns: list[str]) -> str:
        return " | ".join(col.ljust(widths[idx]) for idx, col in enumerate(columns))

    divider = "-+-".join("-" * width for width in widths)
    lines = [format_row(headers), divider]
    lines.extend(format_row(row) for row in string_rows)
    return "\n".join(lines)


def print_schedule(schedule: list[Task]) -> None:
    print_section("Today's Schedule")
    if not schedule:
        print("No tasks fit within today's available time.")
        return

    rows = []
    total_minutes = sum(task.duration for task in schedule)
    for index, task in enumerate(schedule, start=1):
        rows.append(
            [
                index,
                task_type_label(task),
                task.description,
                task.pet_name or "Unassigned",
                task.time or "--:--",
                task.duration,
                PRIORITY_BADGES.get(task.priority, task.priority.title()),
                STATUS_BADGES[task.completed],
            ]
        )

    print(render_table(rows, ["#", "Type", "Task", "Pet", "Time", "Minutes", "Priority", "Status"]))

    print(f"Total scheduled: {total_minutes} minutes")


def print_task_list(title: str, tasks: list[Task]) -> None:
    print_section(title)
    if not tasks:
        print("No tasks to show.")
        return

    rows = []
    for index, task in enumerate(tasks, start=1):
        rows.append(
            [
                index,
                task_type_label(task),
                task.description,
                task.pet_name or "Unassigned",
                task.time or "--:--",
                task.duration,
                PRIORITY_BADGES.get(task.priority, task.priority.title()),
                STATUS_BADGES[task.completed],
            ]
        )

    print(render_table(rows, ["#", "Type", "Task", "Pet", "Time", "Minutes", "Priority", "Status"]))


def main() -> None:
    owner = Owner(name="Ananya", daily_time_available=2.0)

    bella = Pet(
        name="Bella",
        species="Dog",
        energy_level="High",
        dietary_needs="High-protein kibble",
        medical_needs="None",
    )
    cheetos = Pet(
        name="Cheetos",
        species="Golden Retriever",
        energy_level="High",
        dietary_needs="Chicken-free food",
        medical_needs="Joint supplements",
    )

    owner.add_pet(bella)
    owner.add_pet(cheetos)

    owner.add_new_task(
        Task(description="Morning Walk", duration=45, time="08:30", frequency="daily", priority="high", category="exercise"),
        pet_name="Bella",
    )
    owner.add_new_task(
        Task(description="Evening Feeding", duration=15, time="18:00", frequency="daily", priority="high", category="feeding"),
        pet_name="Cheetos",
    )
    owner.add_new_task(
        Task(description="Puzzle Play", duration=30, time="12:15", frequency="daily", priority="medium", category="enrichment"),
        pet_name="Cheetos",
    )
    owner.add_new_task(
        Task(description="Brush Coat", duration=25, time="07:45", frequency="weekly", priority="low", category="grooming"),
        pet_name="Bella",
    )
    owner.add_new_task(
        Task(description="Medication", duration=10, time="06:30", frequency="daily", priority="high", category="medical", completed=True),
        pet_name="Cheetos",
    )
    owner.add_new_task(
        Task(description="Quick Training", duration=20, time="08:30", frequency="daily", priority="medium", category="training"),
        pet_name="Bella",
    )
    owner.add_new_task(
        Task(description="Vet Call", duration=15, time="08:30", frequency="as needed", priority="high", category="medical"),
        pet_name="Cheetos",
    )

    all_tasks = owner.get_all_tasks(include_completed=True)
    print_task_list("All Tasks (Added Out of Order)", all_tasks)

    sorted_by_time = owner.scheduler.sort_by_time(all_tasks)
    print_task_list("Sorted by Time (HH:MM)", sorted_by_time)

    bella_pending = owner.scheduler.filter_tasks(all_tasks, completed=False, pet_name="Bella")
    print_task_list("Filtered: Bella + Pending", bella_pending)

    completed_tasks = owner.scheduler.filter_tasks(all_tasks, completed=True)
    print_task_list("Filtered: Completed Tasks", completed_tasks)

    conflict_warnings = owner.scheduler.detect_time_conflicts(all_tasks)
    print_section("Conflict Warnings")
    if not conflict_warnings:
        print("🟢 No time conflicts detected.")
    else:
        for warning in conflict_warnings:
            print(f"🔵 {warning}")

    morning_walk = next(task for task in all_tasks if task.description == "Morning Walk")
    brush_coat = next(task for task in all_tasks if task.description == "Brush Coat")
    next_daily = owner.mark_task_complete(morning_walk)
    next_weekly = owner.mark_task_complete(brush_coat)

    print_section("Recurring Task Auto-Creation")
    if next_daily is not None:
        print(f"🔷 Created next daily task due on: {next_daily.due_date}")
    if next_weekly is not None:
        print(f"🟩 Created next weekly task due on: {next_weekly.due_date}")

    schedule = owner.generate_plan()
    print_schedule(schedule)


if __name__ == "__main__":
    main()
