from datetime import datetime, timedelta

# Current month displayed as string
current_month_displayed = "February"

# Extract the month and year
current_displayed_date = datetime.strptime(current_month_displayed, "%B")
next_month = (current_displayed_date.replace(day=1) + timedelta(days=32)).replace(day=1)

# Convert the next month to a string
next_month_str = next_month.strftime("%B")

print("Next month:", next_month_str)
