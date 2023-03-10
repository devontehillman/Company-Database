import datetime
from dateutil.parser import parse

userstring = "12/2/1990"

dt = parse(userstring)

print(dt.strftime('%m/%d/%Y'))

print(datetime.date.today())