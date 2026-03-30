from pawpal_system import Owner, Pet, Task


def print_schedule(schedule: list[Task]) -> None:
    print("\nToday's Schedule")
    print("-" * 56)
    if not schedule:
        print("No tasks fit within today's available time.")
        return

    total_minutes = 0
    for index, task in enumerate(schedule, start=1):
        total_minutes += task.duration
        pet_label = task.pet_name or "Unassigned"
        print(
            f"{index:>2}. {task.description:<20} | {task.duration:>3} min | "
            f"{task.priority.capitalize():<6} | {task.frequency:<7} | {pet_label}"
        )

    print("-" * 56)
    print(f"Total scheduled: {total_minutes} minutes")


def print_task_list(title: str, tasks: list[Task]) -> None:
    print(f"\n{title}")
    print("-" * 74)
    if not tasks:
        print("No tasks to show.")
        return

    for index, task in enumerate(tasks, start=1):
        time_label = task.time if task.time is not None else "--:--"
        pet_label = task.pet_name or "Unassigned"
        status_label = "done" if task.completed else "pending"
        print(
            f"{index:>2}. {time_label} | {task.description:<18} | {pet_label:<8} | {status_label:<7} | {task.duration:>3} min"
        )


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
    print("\nConflict Warnings")
    print("-" * 74)
    if not conflict_warnings:
        print("No time conflicts detected.")
    else:
        for warning in conflict_warnings:
            print(warning)

    morning_walk = next(task for task in all_tasks if task.description == "Morning Walk")
    brush_coat = next(task for task in all_tasks if task.description == "Brush Coat")
    next_daily = owner.mark_task_complete(morning_walk)
    next_weekly = owner.mark_task_complete(brush_coat)

    print("\nRecurring Task Auto-Creation")
    print("-" * 74)
    if next_daily is not None:
        print(f"Created next daily task due on: {next_daily.due_date}")
    if next_weekly is not None:
        print(f"Created next weekly task due on: {next_weekly.due_date}")

    schedule = owner.generate_plan()
    print_schedule(schedule)


if __name__ == "__main__":
    main()
