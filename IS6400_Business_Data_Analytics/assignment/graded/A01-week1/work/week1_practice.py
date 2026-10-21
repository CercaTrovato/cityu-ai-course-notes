"""Runnable, synthetic-data walkthrough of Tutorial 1 assignment Q1-Q4.

This is a teaching example, not the student's historical submission.
Run: D:\\anaconda3\\python.exe -X utf8 week1_practice.py
"""

import datetime
import time

import numpy as np
import pandas as pd


# These are synthetic examples. Replace them with your own values only in a new personal exercise.
student_id = "DEMO_ID"
student_name = "DEMO_NAME"
first_time = datetime.datetime.now()
print("Q1:", student_id, student_name, first_time)

# Q2: include numeric score and grade columns now, so Q4 has a clear input.
table = pd.DataFrame(
    columns=["id", "name", "time", "score", "grade"]
)
table.loc[0] = [student_id, student_name, first_time, 80, 1]
print("Q2:\n", table)

# Q3: take the clock reading again after a few seconds.
time.sleep(3)
second_time = datetime.datetime.now()
table.loc[1] = [student_id, student_name, second_time, 90, 1]
assert second_time > first_time
assert len(table) == 2
print("Q3:\n", table)

# Q4: select only score and grade; do not pass names or datetime to numeric NumPy operations.
matrix = table[["score", "grade"]].to_numpy(dtype=float)
assert matrix.shape == (2, 2)
print("Q4 matrix:\n", matrix)
print("Q4 transpose:\n", matrix.T)
print("Q4 score sum:", np.sum(matrix[:, 0]))
