# Set the correct Python version info to the environment variable which controls
# the used Python interpreter, make the compiler output release binaries, and
# activate rustimport's import hook. This enables automatic compilation for the
# Python version that this script is started with. However, this has not yet
# been tested with systems like pyenv.
# Do note that this requires `rustimport` Python package and Rust's Cargo to be
# up-to-date.
import os
import sys
os.environ["PYO3_PYTHON"] = (
    f"python{sys.version_info.major}.{sys.version_info.minor}"
)
os.environ["RUSTIMPORT_RELEASE_BINARIES"] = "true"
import rustimport.import_hook

# --------------------------- PLACE YOUR CODE BELOW --------------------------- #

import rustexample
import numpy as np
import time

test = rustexample.TestClass(123)
test.join()
print(f"123 + 77 = {test.add(77)}")

vec = np.random.randint(-1000, 1000, size=(1000,), dtype=np.int64)
mat = np.random.randint(0, 255, size=(1200, 1600), dtype=np.uint8)

ITERATIONS_PY = 10
ITERATIONS_RS = 10
ITERATIONS_NP = 10


# Loop with Python
start = time.time()
for _ in range(ITERATIONS_PY):
    total = 0
    for row in range(mat.shape[0]):
        for col in range(mat.shape[1]):
            total += mat[row, col]
duration_py = (time.time() - start) / ITERATIONS_PY

# Loop with Rust
start = time.time()
for _ in range(ITERATIONS_RS):
    total = rustexample.sum_mat(mat)
duration_rs = (time.time() - start) / ITERATIONS_RS

# Use Numpy's internal .sum() method
start = time.time()
for _ in range(ITERATIONS_NP):
    total = mat.sum()
duration_np = (time.time() - start) / ITERATIONS_NP

# Show results
print()
print("Matrix sum speed")
print(f"  Python: {duration_py*1000:.3f} ms")
print(f"  Rust:   {duration_rs*1000:.3f} ms")
print(f"  Numpy:  {duration_np*1000:.3f} ms")
