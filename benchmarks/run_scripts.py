import subprocess

params = [("20", "100"), ("20", "190"), ("30", "150"), ("30", "300"), ("100", "500"), ("100", "1000"), ("200", "300"), ("200", "400"), ("200", "1000"), ("1000", "4000")]


for param, value in params:
    subprocess.call(["python3", "edges_sampling_parallel.py", param, value])
