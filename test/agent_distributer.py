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
    pool.add_member(host='rubberduck')
    for member in pool.members:
        print(pool.members[member].to_dict())
    print(pool.local_member.to_dict())