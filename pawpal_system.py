from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pet:
	name: str
	species: str
	energy_level: str
	dietary_needs: str
	medical_needs: str
	other_notes: str = ""

	def update_profile(self) -> None:
		pass

	def get_needs_summary(self) -> str:
		pass


@dataclass
class Task:
	description: str
	duration: int
	priority: str
	category: str
	pet_name: Optional[str] = None

	def edit_task(self) -> None:
		pass

	def get_critical_task(self) -> bool:
		pass


class Scheduler:
	def __init__(self, time_available: float, task_list: Optional[List[Task]] = None) -> None:
		self.time_available = time_available
		# Share task storage with Owner to avoid duplicate sources of truth.
		self.task_list: List[Task] = task_list if task_list is not None else []

	def add_new_task(self, task: Task) -> None:
		pass

	def set_daily_limit(self, hours: float) -> None:
		pass

	def edit_schedule(self) -> None:
		pass

	def generate_plan(self, owner: "Owner", pets: List[Pet]) -> List[Task]:
		pass


class Owner:
	def __init__(self, name: str, daily_time_available: float) -> None:
		self.name = name
		self.daily_time_available = daily_time_available
		self.pets: List[Pet] = []
		self.tasks: List[Task] = []
		self.scheduler = Scheduler(daily_time_available, self.tasks)

	def add_pet(self, pet: Pet) -> None:
		pass

	def add_new_task(self, task: Task) -> None:
		pass

	def generate_plan(self) -> List[Task]:
		pass

	def explain_plan(self) -> str:
		pass
