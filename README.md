# Employee Leave Management System

A simple, menu-based Python program to add employees, submit leave requests,
approve requests, and check remaining leave balances. It uses only Python's
standard library and saves information in `leave_data.json`.

## Run

```text
python3 main.py
```

Choose an option from the menu. Add an employee first, then apply for leave
using dates in `YYYY-MM-DD` format. Leave days include both the start and end
date, and weekends are counted.

Each employee starts with 20 annual, 10 sick, and 5 personal leave days.
Pending requests reserve days; approved requests use them. The program saves
after employee and request changes.

Run the basic balance test with:

```text
python3 -m unittest
```