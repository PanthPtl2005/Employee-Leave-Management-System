"""Basic tests for leave balance calculations."""

from main import edit_leave_request, get_balance


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


def test_edit_pending_request_updates_type_and_dates(monkeypatch):
    data = {
        "employees": {"E001": "Avery"},
        "requests": [
            {
                "id": 1,
                "employee_id": "E001",
                "leave_type": "annual",
                "start": "2026-12-01",
                "end": "2026-12-03",
                "days": 3,
                "status": "pending",
            }
        ],
    }
    answers = iter(["1", "sick", "2026-12-10", "2026-12-14"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr("main.save_data", lambda _: None)

    edit_leave_request(data)

    request = data["requests"][0]
    assert request["leave_type"] == "sick"
    assert request["start"] == "2026-12-10"
    assert request["end"] == "2026-12-14"
    assert request["days"] == 5
    assert request["status"] == "pending"
    assert get_balance(data, "E001") == {
        "annual": 20,
        "sick": 5,
        "personal": 5,
    }


def test_editing_approved_request_does_not_change_it(monkeypatch, capsys):
    request = {
        "id": 1,
        "employee_id": "E001",
        "leave_type": "annual",
        "start": "2026-12-01",
        "end": "2026-12-03",
        "days": 3,
        "status": "approved",
    }
    data = {"employees": {"E001": "Avery"}, "requests": [request]}
    monkeypatch.setattr("builtins.input", lambda _: "1")

    edit_leave_request(data)

    assert request["leave_type"] == "annual"
    assert request["days"] == 3
    assert "Pending request not found." in capsys.readouterr().out
