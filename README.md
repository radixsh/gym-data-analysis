# Analyzing GymRoutines data
This is a script I created to analyze my data from going to the gym. It reads
SQLite3 data and graphs improvement over time, outputting `png` images generated
by matplotlib.

To log my workouts, I've been using a free and open-source Android app called
[GymRoutines](https://codeberg.org/noahjutz/GymRoutines). I tried a couple
different apps, but I settled on GymRoutines because of how its workflow feels,
as well as because of its transparent data export option.

After going to the gym this morning, I decided I wanted to see how much I'd
progressed over the past few months. I had a bit of experience with MongoDB but
absolutely no experience with relational databases, so it wasn't easy to figure
out how these different tables mapped to one another. However, I was focused and
determined after going to the gym, and Python helpfully had a library called
`sqlite3` I could use. Now, about eight hours later, I've learned how SQLite3
databases work, and I've been able to create some nice graphs and plots with
`matplotlib` to see my gym progress!

I used [my old biology scripts](https://github.com/radixsh/bis-2b) as a base
from which to build my plotting things. Maybe this repo, too, will be helpful
for me in the future if I work with SQLite3 again.

## Running the script
Assuming the data from GymRoutines is in `gym_data.db`, you can run this script
on it with `./analyze.py gym_data.db`.

By default, this script will look for bench press, deadlift, and barbell squat
data, but you can specify targets by editing the script. For each exercise, it
will graph weight and force in separate graphs. Weight is just weight, while
force accounts for the fact that maybe you're not lifting more weight, but you
are doing more reps of that heavy weight.
