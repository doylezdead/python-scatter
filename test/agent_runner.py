from scatter.models.pool import Pool
import random


def print_rand():
    val = random.randint(1, 10)
    print(val)
    return val


def print_passed(val=0):
    print(val)
    # time.sleep(1)
    return val

if __name__ == '__main__':
    pool = Pool()
    pool.listen_loop()
