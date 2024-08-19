import sys
import sqlite3
import matplotlib as mpl 
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

def graph_data(data):
    print('Data to be graphed:')
    pprint(data)

    plt.xlabel('Timestamp')
    plt.ylabel('Weight')

    timespan = [x[0] for x in data]
    weights = [x[1] for x in data]

    # https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.Normalize.html#matplotlib.colors.Normalize
    reps = [x[2] for x in data]
    norm = mpl.colors.Normalize(vmin=0, vmax=1, clip=False)

    plt.scatter(timespan, weights, c=norm(reps))    #label="Bench press", c=norm(reps))

    # plt.legend()#bbox_to_anchor=(1,1), loc="upper right")
    plt.savefig("bench_press.png")#, bbox_inches="tight")
    plt.show()

def show_all_tables(conn):
    tables = [#'exercise_table', 
              'workout_table',
              'routine_set_table', 'routine_set_group_table',
              'workout_set_table', 'workout_set_group_table'
              ]
    for table in tables:
        print(table)
        count = 0
        for row in conn.execute(f"SELECT * FROM {table}"):
            count += 1
            if count >= 10:
                break
            print(row)
        print()
    print('\n')

def find_exercise_data(exercise_name, conn):
    res = conn.execute(f"SELECT * FROM exercise_table WHERE name == '{exercise_name}'")
    exercise_id = res.fetchone()['exerciseId']

    ids = []
    print(f'Seeking bench_press (ID={exercise_id}) data in workout_set_group_table')
    for row in conn.execute(f"SELECT * FROM workout_set_group_table"):
        if row['exerciseId'] == exercise_id:
            ids.append(row['id'])
            pprint(row)
    print(f'ids: {ids}')

    data = []
    print('\nworkout_set_table')
    index = 0
    for row in conn.execute(f"SELECT * FROM workout_set_table"):
        index += 1
        
        # groupId identifies a unique combination of workout ID and exercise ID
        if not (row['groupId'] in ids and row['complete']):
            continue 
        print(f'workout_set_table row: {row}')

        # Find timestamp
        j = 1       # Account for index incrementing at start of 'for' loop
        for row in conn.execute(f"SELECT * FROM routine_set_table"):
            if j == index:
                group_id = row['groupId']
                print(f'routine_set_table row: {row}')
                break
            j += 1

        cmd = f"SELECT * FROM routine_set_group_table WHERE id == '{group_id}'"
        workout_id = conn.execute(cmd).fetchone()['routineId']
        
        cmd = f"SELECT * FROM workout_table WHERE routineId == '{workout_id}'"
        timestamp = conn.execute(cmd).fetchone()['startTime']
        
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
        timestamp = datetime.fromtimestamp(timestamp / 1e3)

        data.append((timestamp, row['weight'], row['reps']))

    return data

def dict_factory(cursor, row):
    # https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
    # https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# Goal: graph change of energy (reps x weight) over time for each exercise
def main():
    try:
        # https://docs.python.org/3/library/sqlite3.html#tutorial
        conn = sqlite3.connect(sys.argv[1])
        conn.row_factory = dict_factory
    except:
        print('Usage: ./analyze.py gymroutines.db')
        sys.exit(0)
    
    show_all_tables(conn)

    # Find data pertaining to 'exercise_name' across all workouts
    data = find_exercise_data('bench press', conn)

    graph_data(data)

if __name__ == "__main__":
    main()
