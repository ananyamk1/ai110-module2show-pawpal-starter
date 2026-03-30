from pawpal_system import Owner, Pet, Task


def print_schedule(owner: Owner, schedule: list[Task]) -> None:
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
		Task(description="Morning Walk", duration=45, frequency="daily", priority="high", category="exercise"),
		pet_name="Bella",
	)
	owner.add_new_task(
		Task(description="Evening Feeding", duration=15, frequency="daily", priority="high", category="feeding"),
		pet_name="Cheetos",
	)
	owner.add_new_task(
		Task(description="Puzzle Play", duration=30, frequency="daily", priority="medium", category="enrichment"),
		pet_name="Cheetos",
	)
	owner.add_new_task(
		Task(description="Brush Coat", duration=25, frequency="weekly", priority="low", category="grooming"),
		pet_name="Bella",
	)

	schedule = owner.generate_plan()
	print_schedule(owner, schedule)


if __name__ == "__main__":
	main()
