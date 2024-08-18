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
 ('workout_table',),
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
 ('index_routine_set_table_groupId',),
 ('routine_set_group_table',),
        [(0, 'routineId', 'INTEGER', 1, None, 0),
         (1, 'exerciseId', 'INTEGER', 1, None, 0),
         (2, 'position', 'INTEGER', 1, None, 0),
         (3, 'id', 'INTEGER', 1, None, 1)]
 ('index_routine_set_group_table_routineId',),
 ('workout_set_table',),
        [(0, 'groupId', 'INTEGER', 1, None, 0),
         (1, 'reps', 'INTEGER', 0, None, 0),
         (2, 'weight', 'REAL', 0, None, 0),
         (3, 'time', 'INTEGER', 0, None, 0),
         (4, 'distance', 'REAL', 0, None, 0),
         (5, 'complete', 'INTEGER', 1, None, 0),
         (6, 'workoutSetId', 'INTEGER', 1, None, 1)]
 ('index_workout_set_table_groupId',),
 ('workout_set_group_table',),
        [(0, 'routineId', 'INTEGER', 1, None, 0),
         (1, 'exerciseId', 'INTEGER', 1, None, 0),
         (2, 'position', 'INTEGER', 1, None, 0),
         (3, 'id', 'INTEGER', 1, None, 1)]
 ('index_workout_set_group_table_workoutId',),
 ('room_master_table',)]
'''

# Goal: graph change of energy (reps x weight) over time for each exercise
def main():
    try:
        # https://docs.python.org/3/library/sqlite3.html#tutorial
        con = sqlite3.connect(sys.argv[1])
        cur = con.cursor()
    except:
        print('Usage: ./gym.py gymroutines.db')
        sys.exit(0)
    
    exercise_name = 'bench press'
    res = cur.execute(f"SELECT * FROM exercise_table WHERE name == '{exercise_name}'")
    exercise_id = list(res.fetchone())[-1]

    table = 'workout_set_group_table'
    # Get headers with PRAGMA table_info({table name})
    # https://stackoverflow.com/questions/947215/how-to-get-a-list-of-column-names-on-sqlite3-database
    res = cur.execute(f'PRAGMA table_info({table})')
    pprint(res.fetchall())

    # Find data pertaining to 'exercise_name' across all workouts
    res = cur.execute(f"SELECT * FROM {table} WHERE exerciseId == '{exercise_id}'")
    pprint(res.fetchall())
    
    # Graph that data 

if __name__ == "__main__":
    main()
