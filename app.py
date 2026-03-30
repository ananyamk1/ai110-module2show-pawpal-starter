import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
daily_hours = st.number_input("Daily time available (hours)", min_value=0.5, max_value=12.0, value=2.0, step=0.5)

# Persist app data across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, daily_time_available=float(daily_hours))

owner: Owner = st.session_state.owner
owner.name = owner_name
owner.daily_time_available = float(daily_hours)

st.markdown("### Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    energy_level = st.selectbox("Energy level", ["low", "medium", "high"], index=1)
    dietary_needs = st.text_input("Dietary needs", value="Not specified")
    medical_needs = st.text_input("Medical needs", value="None")
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    else:
        try:
            owner.add_pet(
                Pet(
                    name=pet_name.strip(),
                    species=species,
                    energy_level=energy_level,
                    dietary_needs=dietary_needs.strip() or "Not specified",
                    medical_needs=medical_needs.strip() or "None",
                )
            )
            st.success(f"Added pet: {pet_name.strip()}")
        except ValueError as exc:
            st.warning(str(exc))

if owner.pets:
    st.write("Registered pets:")
    st.table(
        [
            {
                "name": pet.name,
                "species": pet.species,
                "energy": pet.energy_level,
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Schedule tasks to specific pets using your backend classes.")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0)
        category = st.text_input("Category", value="general")
        pet_choice = st.selectbox("Assign to pet", [pet.name for pet in owner.pets])
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        owner.add_new_task(
            Task(
                description=task_title.strip() or "Untitled task",
                duration=int(duration),
                priority=priority,
                frequency=frequency,
                category=category.strip() or "general",
            ),
            pet_name=pet_choice,
        )
        st.success(f"Added task '{task_title.strip() or 'Untitled task'}' for {pet_choice}.")
else:
    st.info("Add a pet first before scheduling tasks.")

task_rows = [
    {
        "pet": task.pet_name,
        "title": task.description,
        "duration_minutes": task.duration,
        "priority": task.priority,
        "completed": task.completed,
    }
    for task in owner.get_all_tasks()
]

if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a plan using the scheduler in your logic layer.")

if st.button("Generate schedule"):
    schedule = owner.generate_plan()
    if not schedule:
        st.warning("No tasks fit in the current daily time window.")
    else:
        st.success("Schedule generated.")
        st.table(
            [
                {
                    "pet": task.pet_name,
                    "task": task.description,
                    "duration_minutes": task.duration,
                    "priority": task.priority,
                }
                for task in schedule
            ]
        )
        st.markdown("### Plan explanation")
        st.code(owner.explain_plan())
