import sys
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
import math

def graph_colors(data, exercise_name):
    plt.xlabel('Timestamp')
    plt.ylabel('Weight')

    timespan = [x[0] for x in data]
    weights = [x[1] for x in data]

    # https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.Normalize.html#matplotlib.colors.Normalize
    reps = [x[2] for x in data]
    norm = mpl.colors.Normalize(vmin=0, vmax=1, clip=False)

    plt.scatter(timespan, weights, c=norm(reps))

    plt.title(exercise_name.title())
    plt.savefig(f'images/{exercise_name}.png')
    plt.show()

def graph_force(data, exercise_name):
    plt.xlabel('Timestamp')
    plt.ylabel('Force (weight x reps)')

    timespan = [x[0] for x in data]
    force = [x[1] * math.log(x[2]) for x in data]

    plt.scatter(timespan, force)

    name = f'{exercise_name} (force)'
    plt.title(name.title())
    plt.savefig(f'images/{name}.png')
    plt.show()

def show_all_tables(conn):
    LIMIT = 10
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
            if count >= LIMIT:
                break
            print(row)
        print()
    print('\n')

def find_exercise_data(exercise_name, conn):
    query = f"SELECT * FROM exercise_table WHERE name == '{exercise_name}'"
    result = conn.execute(query).fetchone()
    if result is None:
        print("Error: no such exercise found")
        sys.exit(0)
    exercise_id = result['exerciseId']

    data = []
    for row in conn.execute(f"SELECT * FROM workout_table"):
        # Original timestamp int is in milliseconds
        timestamp = datetime.fromtimestamp(row['startTime'] / 1e3)

        workout_id = row['workoutId']

        query = f"SELECT * FROM workout_set_group_table \
                WHERE workoutId == {workout_id} \
                AND exerciseId == {exercise_id}"
        result = conn.execute(query).fetchone()
        if result is None:
            continue
        print(f'{timestamp.date()}: {result}')
        to_seek = result['id']

        query = f"SELECT * FROM workout_set_table WHERE groupId == '{to_seek}'"
        for row in conn.execute(query):
            print(row)
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

    # For debugging
    # show_all_tables(conn)

    exercises = ['bench press', 'deadlifts', 'barbell squat']
    for exercise_name in exercises:
        data = find_exercise_data(exercise_name, conn)
        
        # Graph weight
        graph_colors(data, exercise_name)

        # Graph force (reps x weight)
        graph_force(data, exercise_name)
    

if __name__ == "__main__":
    main()
