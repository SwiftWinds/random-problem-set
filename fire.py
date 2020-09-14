import itertools
import random
import click
from functional import seq


def ordinal(num):
    "%d%s" % (num, "tsnrhtdd"[(num//10 % 10 != 1)*(num % 10 < 4)*num % 10::4])

def string_range_to_list(my_str):
    print("The original string is : " + my_str) 
    temp = [(lambda sub: range(sub[0], sub[-1] + 1))(list(map(int, ele.split('-')))) for ele in my_str.split(', ')] 
    res = [b for a in temp for b in a]
    print("List after converting it from string : " + str(res)) 
    return res


@click.command()
@click.option('--count', prompt='Number of problems you want',
              help='Number of random problems to generate.')
@click.option('--file', prompt='File describing problem set',
              help='Input file describing the problem set.', type=click.File())
def generate_random_problems(count, file):
    """Simple program that greets NAME for a total of COUNT times."""
    chapters = file.read()

    problems = seq(chapters)\
        .map(lambda chapter: chapter.split(": ", 1))\
        .map(lambda chapter: [chapter[0], string_range_to_list(chapter[1])])\
        .map(lambda chapter: [chapter[0],
                              seq(chapter[1]).map(lambda problem: f"{chapter[0]}: {problem}").to_list()])\
        .map(lambda chapter: chapter[1])\
        .flatten()\
        .to_list()

    random_problem_set = random.sample(problems, count)
    for idx, problem in enumerate(random_problem_set):
        click.echo(f"{ordinal(idx)} problem is {problem}")
    return random_problem_set


if __name__ == '__main__':
    generate_random_problems()
