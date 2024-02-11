from datetime import datetime, timedelta

next_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%B")
print("Next month:", next_month)
