import math
import sys

import pandas as pd

def change_terminal(terminal, T1, T2):
    return T2 if terminal == T1 else T1

def generate_start_times(route_no, num_schedules, trip_duration, headway, no_of_trips_to_offset, start_time, T1, T2, depot1, depot2):
    schedules = [f"{route_no}0{1 + i}" for i in range(num_schedules)]
    T1_trips = math.ceil(num_schedules / 2)
    T2_trips = int(num_schedules / 2)
    df = pd.DataFrame()
    df['schedules'] = schedules
    df['virtual_terminal'] = [T1 for i in range(T1_trips)] + [T2 for i in range(T2_trips)]

    # start time
    if num_schedules % 2 == 0:
        df['start_time'] = [start_time + (headway * i) for i in range(T1_trips)] + [start_time + (headway * i) for i in
                                                                                    range(T2_trips)]
    else:
        df['start_time'] = [start_time + (headway * i) for i in range(T1_trips)] + [
            start_time + headway / 2 + (headway * i) for i in range(T2_trips)]
    df['corrected_start_time'] = [
        time_ + (trip_duration * no_of_trips_to_offset) if i in list(range(1, max(df.index) + 1, 2)) else time_ for
        i, time_ in zip(df.index, df['start_time'])]

    # terminals to start
    if no_of_trips_to_offset % 2 != 0:
        df['corrected_terminal'] = [change_terminal(terminal, T1, T2) if i in list(range(1, max(df.index) + 1, 2)) else terminal
                                    for i, terminal in zip(df.index, df['virtual_terminal'])]
    else:
        df['corrected_terminal'] = df['virtual_terminal'].copy()
    df['depot'] = [depot1 if terminal == T1 else depot2 for terminal in df['corrected_terminal']]
    print(df)
    return df
