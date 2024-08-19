import sys
import sqlite3
import matplotlib as mpl 
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

def dict_factory(cursor, row):
    # https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
    # https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# Goal: graph change of energy (reps x weight) over time for each exercise
def main():
    try:
        # https://docs.python.org/3/library/sqlite3.html#tutorial
        con = sqlite3.connect(sys.argv[1])
        con.row_factory = dict_factory
    except:
        print('Usage: ./analyze.py gymroutines.db')
        sys.exit(0)
    
    exercise_name = 'bench press'
    res = con.execute(f"SELECT * FROM exercise_table WHERE name == '{exercise_name}'")
    exercise_id = res.fetchone()['exerciseId']

    tables = [#'exercise_table', 
              #'workout_table',
              #'routine_set_table', 'routine_set_group_table',
              #'workout_set_table', 'workout_set_group_table'
              ]
    for table in tables:
        print(table)
        count = 0
        for row in con.execute(f"SELECT * FROM {table}"):
            count += 1
            if count >= 10:
                break
            print(row)
        print()

    print('\n')


    # Find data pertaining to 'exercise_name' across all workouts
    ids = []
    print(f'Seeking bench_press (ID={exercise_id}) data in workout_set_group_table')
    for row in con.execute(f"SELECT * FROM workout_set_group_table"):
        if row['exerciseId'] == exercise_id:
            ids.append(row['id'])
            pprint(row)
    print(f'ids: {ids}')

    data = []
    print('\nworkout_set_table')
    index = 0
    for row in con.execute(f"SELECT * FROM workout_set_table"):
        index += 1
        
        # groupId identifies a unique combination of workout ID and exercise ID
        if not (row['groupId'] in ids and row['complete']):
            continue 
        print(f'workout_set_table row: {row}')

        # Find timestamp
        j = 1       # Account for index incrementing at start of 'for' loop
        for row in con.execute(f"SELECT * FROM routine_set_table"):
            if j == index:
                group_id = row['groupId']
                print(f'routine_set_table row: {row}')
                break
            j += 1
        
        cmd = f"SELECT * FROM routine_set_group_table WHERE id == '{group_id}'"
        workout_id = con.execute(cmd).fetchone()['routineId']
        
        cmd = f"SELECT * FROM workout_table WHERE routineId == '{workout_id}'"
        timestamp = con.execute(cmd).fetchone()['startTime']

        # Append a tuple to our data 
        data.append((datetime.fromtimestamp(timestamp / 1e3), row['weight'], row['reps']))
        print()

    print(f'data: {data}')

    # Graph our data 
    plt.xlabel('Timestamp')
    plt.ylabel('Weight')

    # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
    # timespan = [datetime.fromtimestamp(x[0] / 1e3) for x in data]
    timespan = [x[0] for x in data]
    weights = [x[1] for x in data]
    reps = [x[2] for x in data]
    norm = mpl.colors.Normalize(vmin=-1, vmax=1, clip=False)
    plt.scatter(timespan, weights, label="alsdkfj", c=norm(reps))
    # plt.plot(timespan, weights)

    # plt.legend(bbox_to_anchor=(1,1), loc="upper right")
    plt.savefig("bench_press.png")#, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
