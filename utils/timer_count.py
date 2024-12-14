import time
from functools import wraps

def timer_count(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tempo para {func.__name__}: {end_time - start_time:.2f} segundos")
        return result
    return wrapper

@timer_count
def example_sum(x, y, range_num=10000000):
    for i in range(range_num):
        pass
    return x + y

if __name__ == "__main__":
    example_sum(5, 5)