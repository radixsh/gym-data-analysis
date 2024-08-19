import sys
import sqlite3
import matplotlib.pyplot as plt
from pprint import pprint

'''
[('android_metadata',),
 ('exercise_table',),
        [(0, 'name', 'TEXT', 1, None, 0),
         (1, 'notes', 'TEXT', 1, "''", 0),
         (2, 'logReps', 'INTEGER', 1, None, 0),
         (3, 'logWeight', 'INTEGER', 1, None, 0),
         (4, 'logTime', 'INTEGER', 1, None, 0),
         (5, 'logDistance', 'INTEGER', 1, None, 0),
         (6, 'hidden', 'INTEGER', 1, None, 0),
         (7, 'exerciseId', 'INTEGER', 1, None, 1)]
 ('sqlite_sequence',),
 ('routine_table',),
        [(0, 'name', 'TEXT', 1, None, 0),
         (1, 'hidden', 'INTEGER', 1, None, 0),
         (2, 'routineId', 'INTEGER', 1, None, 1)]
 ('workout_table',),            # General log of all workouts (+ duration)
        [(0, 'routineId', 'INTEGER', 1, None, 0),
         (1, 'startTime', 'INTEGER', 1, None, 0),
         (2, 'endTime', 'INTEGER', 1, None, 0),
         (3, 'workoutId', 'INTEGER', 1, None, 1)]
 ('routine_set_table',),
        [(0, 'groupId', 'INTEGER', 1, None, 0),
         (1, 'reps', 'INTEGER', 0, None, 0),
         (2, 'weight', 'REAL', 0, None, 0),
         (3, 'time', 'INTEGER', 0, None, 0),
         (4, 'distance', 'REAL', 0, None, 0),
         (5, 'routineSetId', 'INTEGER', 1, None, 1)]
 ('routine_set_group_table',),
        [(0, 'routineId', 'INTEGER', 1, None, 0),
         (1, 'exerciseId', 'INTEGER', 1, None, 0),
         (2, 'position', 'INTEGER', 1, None, 0),
         (3, 'id', 'INTEGER', 1, None, 1)]
 ('workout_set_table',),
        [(0, 'groupId', 'INTEGER', 1, None, 0),
         (1, 'reps', 'INTEGER', 0, None, 0),
         (2, 'weight', 'REAL', 0, None, 0),
         (3, 'time', 'INTEGER', 0, None, 0),
         (4, 'distance', 'REAL', 0, None, 0),
         (5, 'complete', 'INTEGER', 1, None, 0),
 ('workout_set_group_table',),
        [(0, 'routineId', 'INTEGER', 1, None, 0),
         (1, 'exerciseId', 'INTEGER', 1, None, 0),
         (2, 'position', 'INTEGER', 1, None, 0),
         (3, 'id', 'INTEGER', 1, None, 1)]
 ('room_master_table',)]
'''

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
              'workout_table',
              'routine_set_table', 'routine_set_group_table',
              'workout_set_table', 'workout_set_group_table']
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

    force = []
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
                # print(f'index = {index}, j = {j}')
                group_id = row['groupId']
                print(f'routine_set_table row: {row}')
                break
            j += 1
        # print(f'Group ID: {group_id}')
        
        cmd = f"SELECT * FROM routine_set_group_table WHERE id == '{group_id}'"
        workout_id = con.execute(cmd).fetchone()['routineId']
        # for row in con.execute(cmd):
        #     print(f'routine_set_group_table row: {row}')
        #     workout_id = row['routineId']
        # for row in con.execute(f"SELECT * FROM routine_set_group_table"):
        #     if row['id'] == group_id:
        #         workout_id = row['workoutId']
        
        cmd = f"SELECT * FROM workout_table WHERE routineId == '{workout_id}'"
        timestamp = con.execute(cmd).fetchone()['startTime']
        # for row in con.execute(cmd):
        #     print(f'Timestamp entry: {row}')
        #     timestamp = row['startTime']

        force.append((row['reps'], row['weight'], timestamp))
        print()

    print(f'force: {force}')


    # Graph that data 
    '''
    timespan = [x for x in range
    plt.scatter(timespan, c, color="orange", label="Weight")

    plt.xlabel('Samples taken')
    plt.ylabel('Total number of species observed')

    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.savefig("succulents.png", bbox_inches="tight")
    plt.show()
    '''


if __name__ == "__main__":
    main()
