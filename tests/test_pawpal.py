from pawpal_system import Pet, Task


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
