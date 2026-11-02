"""Basic tests for leave balance calculations."""

from main import get_balance


def test_pending_and_approved_leave_reduce_balance():
    data = {
        "requests": [
            {
                "employee_id": "E001",
                "leave_type": "annual",
                "days": 3,
                "status": "approved",
            },
            {
                "employee_id": "E001",
                "leave_type": "annual",
                "days": 2,
                "status": "pending",
            },
            {
                "employee_id": "E001",
                "leave_type": "sick",
                "days": 1,
                "status": "rejected",
            },
        ]
    }

    assert get_balance(data, "E001") == {
        "annual": 15,
        "sick": 10,
        "personal": 5,
    }
