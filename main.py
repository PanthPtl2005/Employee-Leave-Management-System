"""A simple menu-based employee leave management system."""

import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("leave_data.json")
ALLOWANCES = {"annual": 20, "sick": 10, "personal": 5}


def load_data():
    """Load saved information, or start with empty employee and request lists."""
    if DATA_FILE.exists():
        with DATA_FILE.open(encoding="utf-8") as file:
            return json.load(file)
    return {"employees": {}, "requests": [], "next_id": 1}


def save_data(data):
    """Save employees and requests so they are available next time."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def add_employee(data):
    employee_id = input("Employee ID: ").strip()
    name = input("Employee name: ").strip()

    if not employee_id or not name:
        print("Employee ID and name are required.")
    elif employee_id in data["employees"]:
        print("That employee ID already exists.")
    else:
        data["employees"][employee_id] = name
        save_data(data)
        print(f"Added {name}.")


def apply_for_leave(data):
    employee_id = input("Employee ID: ").strip()
    if employee_id not in data["employees"]:
        print("Employee not found. Add the employee first.")
        return

    leave_type = input("Leave type (annual, sick, personal): ").strip().lower()
    if leave_type not in ALLOWANCES:
        print("Please choose annual, sick, or personal.")
        return

    try:
        start_text = input("Start date (YYYY-MM-DD): ").strip()
        end_text = input("End date (YYYY-MM-DD): ").strip()
        start = date.fromisoformat(start_text)
        end = date.fromisoformat(end_text)
        if start.isoformat() != start_text or end.isoformat() != end_text:
            raise ValueError
        if end < start:
            print("End date must be on or after the start date.")
            return
    except ValueError:
        print("Please enter dates in YYYY-MM-DD format.")
        return

    days = (end - start).days + 1
    balance = get_balance(data, employee_id)[leave_type]
    if days > balance:
        print(f"Not enough leave. {balance} {leave_type} day(s) available.")
        return

    request = {
        "id": data["next_id"],
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "days": days,
        "status": "pending",
    }
    data["requests"].append(request)
    data["next_id"] += 1
    save_data(data)
    print(f"Leave request #{request['id']} submitted for approval.")


def approve_leave(data):
    show_requests(data, pending_only=True)
    request_id = input("Request number to approve: ").strip()

    for request in data["requests"]:
        if str(request["id"]) == request_id and request["status"] == "pending":
            request["status"] = "approved"
            save_data(data)
            print(f"Request #{request_id} approved.")
            return

    print("Pending request not found.")


def get_balance(data, employee_id):
    """Return each leave type's remaining days, including pending requests."""
    balance = ALLOWANCES.copy()
    for request in data["requests"]:
        if (
            request["employee_id"] == employee_id
            and request["status"] in ("pending", "approved")
        ):
            balance[request["leave_type"]] -= request["days"]
    return balance


def check_balance(data):
    employee_id = input("Employee ID: ").strip()
    if employee_id not in data["employees"]:
        print("Employee not found.")
        return

    print(f"Leave balance for {data['employees'][employee_id]}:")
    for leave_type, days in get_balance(data, employee_id).items():
        print(f"  {leave_type.title()}: {days} day(s)")


def show_requests(data, pending_only=False):
    requests = data["requests"]
    if pending_only:
        requests = [item for item in requests if item["status"] == "pending"]

    if not requests:
        print("No leave requests.")
        return

    for request in requests:
        name = data["employees"][request["employee_id"]]
        print(
            f"#{request['id']} {name} | {request['leave_type']} | "
            f"{request['start']} to {request['end']} | "
            f"{request['days']} day(s) | {request['status']}"
        )


def main():
    data = load_data()
    actions = {
        "1": add_employee,
        "2": apply_for_leave,
        "3": approve_leave,
        "4": check_balance,
        "5": show_requests,
    }

    while True:
        print("\nEmployee Leave Management")
        print("1. Add employee")
        print("2. Apply for leave")
        print("3. Approve leave")
        print("4. Check leave balance")
        print("5. List leave requests")
        print("0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        if choice in actions:
            actions[choice](data)
        else:
            print("Please choose a number from 0 to 5.")


if __name__ == "__main__":
    main()
