from dict_diff import *
from test_dict_diff import test_cases
import cProfile

def run_n_times(n=100):
    for i in range(n):
        for test in test_cases:
            dict_diff(test["orig"], test["new"], removing=False)

if __name__ == "__main__":
    cProfile.run('run_n_times(n=10000)')
