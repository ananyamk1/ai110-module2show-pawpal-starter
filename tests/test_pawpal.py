from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task


def test_task_mark_complete_sets_completed_true() -> None:
    task = Task(description="Morning Walk", duration=30)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet_increases_task_count() -> None:
    pet = Pet(
        name="Bella",
        species="Dog",
        energy_level="High",
        dietary_needs="Standard kibble",
        medical_needs="None",
    )
    task = Task(description="Evening Feeding", duration=15)

    before_count = len(pet.tasks)
    pet.add_task(task)
    after_count = len(pet.tasks)

    assert after_count == before_count + 1


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    tasks = [
        Task(description="Lunch", duration=30, time="12:00"),
        Task(description="Morning Walk", duration=30, time="08:30"),
        Task(description="Evening Meds", duration=15, time="18:15"),
    ]

    ordered_tasks = owner.scheduler.sort_by_time(tasks)

    assert [task.time for task in ordered_tasks] == ["08:30", "12:00", "18:15"]
    assert [task.description for task in ordered_tasks] == [
        "Morning Walk",
        "Lunch",
        "Evening Meds",
    ]


def test_mark_task_complete_creates_next_daily_task() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    pet = Pet(
        name="Bella",
        species="Dog",
        energy_level="High",
        dietary_needs="Standard kibble",
        medical_needs="None",
    )
    owner.add_pet(pet)
    daily_task = Task(description="Morning Walk", duration=30, frequency="daily")
    owner.add_new_task(daily_task, pet_name="Bella")

    next_task = owner.mark_task_complete(daily_task)

    assert next_task is not None
    assert daily_task.completed is True
    assert next_task.frequency == "daily"
    assert next_task.pet_name == "Bella"
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_mark_task_complete_creates_next_weekly_task() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    pet = Pet(
        name="Cheetos",
        species="Dog",
        energy_level="High",
        dietary_needs="Chicken-free food",
        medical_needs="Joint supplements",
    )
    owner.add_pet(pet)
    weekly_task = Task(description="Brush Coat", duration=20, frequency="weekly")
    owner.add_new_task(weekly_task, pet_name="Cheetos")

    next_task = owner.mark_task_complete(weekly_task)

    assert next_task is not None
    assert weekly_task.completed is True
    assert next_task.frequency == "weekly"
    assert next_task.pet_name == "Cheetos"
    assert next_task.due_date == date.today() + timedelta(days=7)
    assert next_task.completed is False


def test_detect_time_conflicts_returns_warning_messages() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    bella = Pet(
        name="Bella",
        species="Dog",
        energy_level="High",
        dietary_needs="Standard kibble",
        medical_needs="None",
    )
    cheetos = Pet(
        name="Cheetos",
        species="Dog",
        energy_level="High",
        dietary_needs="Chicken-free food",
        medical_needs="Joint supplements",
    )
    owner.add_pet(bella)
    owner.add_pet(cheetos)

    owner.add_new_task(Task(description="Morning Walk", duration=30, time="08:30", frequency="daily"), pet_name="Bella")
    owner.add_new_task(Task(description="Vet Call", duration=15, time="08:30", frequency="as needed"), pet_name="Cheetos")

    warnings = owner.scheduler.detect_time_conflicts(owner.get_all_tasks(include_completed=True))

    assert len(warnings) == 1
    assert "08:30" in warnings[0]
    assert "Morning Walk" in warnings[0]
    assert "Vet Call" in warnings[0]


def test_find_next_available_slot_returns_earliest_gap() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    tasks = [
        Task(description="Morning Walk", duration=30, time="08:00"),
        Task(description="Breakfast", duration=30, time="09:00"),
    ]

    slot = owner.scheduler.find_next_available_slot(
        tasks,
        required_duration=20,
        day_start="07:00",
        day_end="10:00",
    )

    assert slot == "07:00"


def test_find_next_available_slot_merges_overlaps_before_searching_gap() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    tasks = [
        Task(description="Task A", duration=40, time="08:00"),
        Task(description="Task B", duration=40, time="08:20"),
        Task(description="Task C", duration=30, time="09:30"),
    ]

    slot = owner.scheduler.find_next_available_slot(
        tasks,
        required_duration=20,
        day_start="08:00",
        day_end="10:30",
    )

    assert slot == "09:00"


def test_find_next_available_slot_returns_none_when_no_gap_fits() -> None:
    owner = Owner(name="Jordan", daily_time_available=2.0)
    tasks = [
        Task(description="Task A", duration=60, time="08:00"),
        Task(description="Task B", duration=60, time="09:00"),
    ]

    slot = owner.scheduler.find_next_available_slot(
        tasks,
        required_duration=30,
        day_start="08:00",
        day_end="10:00",
    )

    assert slot is None
