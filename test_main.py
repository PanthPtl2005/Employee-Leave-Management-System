"""Basic tests for leave balance calculations."""

import unittest

from main import get_balance


class LeaveBalanceTests(unittest.TestCase):
    def test_pending_and_approved_leave_reduce_balance(self):
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

        self.assertEqual(get_balance(data, "E001"), {
            "annual": 15,
            "sick": 10,
            "personal": 5,
        })


if __name__ == "__main__":
    unittest.main()
