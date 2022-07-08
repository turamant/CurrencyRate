from datetime import datetime

file_name = 'exact_{}.csv'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
dt = datetime.now()
dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")

for i in range(4):
    print(file_name)

print(dt_string)
print(datetime.now())