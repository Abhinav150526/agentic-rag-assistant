from datetime import date

def calculate_remaining_leave_days(employee_name):
    total_leave = 20

    used_leave = {
        "abhi": 8,
        "john": 12,
        "sarah": 5
    }

    employee_name = employee_name.lower()

    if employee_name not in used_leave:
        return "Employee not found."

    remaining = total_leave - used_leave[employee_name]

    return f"{employee_name.title()} has {remaining} leave days remaining."

def get_current_date():
    today = date.today()
    return f"Today's date is {today}."

def calculate(expression):
    try:
        result = eval(expression)
        return f"The calculation result is {result}."
    except Exception:
        return "I could not calculate that expression."

def get_remaining_leave_days(employee_name):
    total_leave = 20

    used_leave = {
        "abhi": 8,
        "john": 12,
        "sarah": 5
    }

    employee_name = employee_name.lower()

    if employee_name not in used_leave:
        return None

    remaining = total_leave - used_leave[employee_name]

    return remaining