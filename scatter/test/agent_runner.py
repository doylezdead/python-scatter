import scatter
import random


def print_rand():
    val = random.randint(1, 10)
    print(val)
    return val


def print_passed(val=0):
    print(val)
    return val

if __name__ == '__main__':
    a = scatter.Agent(target=print_passed)
    a.listen()
