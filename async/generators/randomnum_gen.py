"""
If a function contains at least one yield statement (it may contain other yield or return statements),
it becomes a generator function.
Both yield and return will return some value from a function.

When a generator function is called, it returns an object (iterator) but does not start execution immediately.

Methods like __iter__() and __next__() are implemented automatically, meaning we can iterate through the items using next()

Local variables and their states are remembered between successive calls

When the function terminates, StopIteration is raised automatically on further calls
"""
import random
from typing import Generator


def random_number_array(n: int, from_num: int, to_num: int) -> Generator:
    for i in range(n):
        yield random.randint(from_num, to_num)



if __name__ == '__main__':
    generator_iterator_from_our_generator_function: Generator = random_number_array(10,0,100)
    for number in generator_iterator_from_our_generator_function:
        print(number)

    print("Printed the last number produced by the generator")
    try:
        print(next(generator_iterator_from_our_generator_function))
    except StopIteration:
        print("Iterator raised StopIteration because we have already iterated over its result")
