import sys
import click
import random
import itertools


def string_range_to_list(my_str):
    print("The original string is : " + my_str)
    temp = [(lambda sub: range(sub[0], sub[-1] + 1))
            (list(map(int, ele.split('-')))) for ele in my_str.split(', ')]
    res = [b for a in temp for b in a]
    print("List after converting it from string : " + str(res))
    return res


@click.command()
@click.option('--count', help='Number of random problems to generate.')
@click.option('--file', type=click.Path(exists=True), help='Input file describing the problem set.')
def generate_random_problems(count, file):
    with open(file, 'r') as input_file:
        click.echo(type(input_file))
        s = input_file.read().splitlines()

        result = list(map(lambda chapter: chapter.split(", ", 1), s))

        click.echo(result)

        result = list(map(lambda chapter: [chapter[0],
                                           string_range_to_list(chapter[1])], result))

        result = list(map(lambda chapter: [chapter[0], list(
            map(lambda problem: chapter[0] + " " + str(problem), chapter[1]))], result))

        result = list(map(lambda chapter: chapter[1], result))

        merged = list(itertools.chain(*result))

        result = []
        for _ in itertools.repeat(None, count):
            selected = random.choice(merged)
            result += selected
            click.echo("random item from list is: ", random.choice(selected))
        return result


if __name__ == '__main__':
    generate_random_problems()
