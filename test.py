import time


def get_time_list(time_type):
    time_list = []
    if time_type == "week":
        for i in range(7):
            time_list.insert(0, time.strftime(
                "%Y-%m-%d", time.localtime(time.time() - i*24*3600)))
    elif time_type == "day":
        for i in range(24):
            time_list.insert(0, time.strftime(
                "%H:00", time.localtime(time.time() - i*3600)))
    return time_list


print(get_time_list("week"))
print(get_time_list("day"))
