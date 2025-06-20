import pandas as pd
import allocation

def generate_schedule(schedule_no, depot, terminal, start_time, shuttle_distance, shuttle_duration, trip_distance,
                      trip_duration, crew_break, crew_half_duration, T1, T2, crew_change, return_time):
    trips_per_half_time = round((crew_half_duration - shuttle_duration) / trip_duration)  # move to route level estimate
    df = pd.DataFrame(
        columns=['schedule_no', 'trip_no', 'event_type', 'origin', 'dest', 'start_time', 'end_time', 'distance',
                 'duration', 'crew_no'])

    trip_count = 1

    end_time = start_time
    start_time = start_time - shuttle_duration
    orig = depot
    dest = terminal

    # crew 1 first half
    df.loc[len(df)] = [schedule_no, trip_count, 'shuttle', orig, dest, start_time, end_time, shuttle_distance,
                       shuttle_duration, 1]
    time = start_time

    for i in range(trips_per_half_time):
        trip_count += 1
        orig = dest
        dest = allocation.change_terminal(orig, T1, T2)
        start_time = end_time
        end_time = start_time + trip_duration

        df.loc[len(df)] = [schedule_no, trip_count, 'trip', orig, dest, start_time, end_time, trip_distance,
                           trip_duration, 1]

    # crew 1 break
    trip_count += 1
    start_time = end_time
    end_time = start_time + crew_break
    orig = dest
    df.loc[len(df)] = [schedule_no, trip_count, 'crew break', orig, dest, start_time, end_time, 0, crew_break, 1]

    # crew 1 second half
    for i in range(trips_per_half_time):
        trip_count += 1
        orig = dest
        dest = allocation.change_terminal(orig, T1, T2)
        start_time = end_time
        end_time = start_time + trip_duration

        df.loc[len(df)] = [schedule_no, trip_count, 'trip', orig, dest, start_time, end_time, trip_distance,
                           trip_duration, 1]

    # crew change
    trip_count += 1
    start_time = end_time
    end_time = start_time + crew_change
    orig = dest
    df.loc[len(df)] = [schedule_no, trip_count, 'crew change', orig, dest, start_time, end_time, 0, crew_change, -1]

    # crew 2 first half
    for i in range(trips_per_half_time):
        trip_count += 1
        orig = dest
        dest = allocation.change_terminal(orig, T1, T2)
        start_time = end_time
        end_time = start_time + trip_duration

        df.loc[len(df)] = [schedule_no, trip_count, 'trip', orig, dest, start_time, end_time, trip_distance,
                           trip_duration, 2]

    # crew 2 break
    trip_count += 1
    start_time = end_time
    end_time = start_time + crew_break
    orig = dest
    df.loc[len(df)] = [schedule_no, trip_count, 'crew break', orig, dest, start_time, end_time, 0, crew_break, 2]

    # crew 2 second half
    for i in range(trips_per_half_time):
        if end_time >= return_time:
            break
        trip_count += 1
        orig = dest
        dest = allocation.change_terminal(orig, T1, T2)
        start_time = end_time
        end_time = start_time + trip_duration
        df.loc[len(df)] = [schedule_no, trip_count, 'trip', orig, dest, start_time, end_time, trip_distance,
                           trip_duration, 2]

    trip_count += 1
    orig = dest
    dest = depot
    print(schedule_no, orig, dest)
    start_time = end_time
    end_time = start_time + shuttle_duration
    df.loc[len(df)] = [schedule_no, trip_count, 'shuttle', orig, dest, start_time, end_time, shuttle_distance,
                       shuttle_duration, 2]
    return df