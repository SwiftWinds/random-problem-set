import random
import click
from functional import seq


def ordinal(num):
    return "%d%s" % (
        num,
        "tsnrhtdd"[(num // 10 % 10 != 1) * (num % 10 < 4) * num % 10 :: 4],
    )


def string_range_to_list(my_str):
    temp = [
        (lambda sub: range(sub[0], sub[-1] + 1))(seq(ele.split("-")).map(int))
        for ele in my_str.split(", ")
    ]
    res = [b for a in temp for b in a]
    return res


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--count",
    prompt="Number of problems you want",
    help="Number of random problems to generate.",
    type=click.IntRange(min=0),
)
@click.option(
    "-f",
    "--file",
    prompt="File describing problem set",
    help="Input file describing the problem set.",
    type=click.File(),
)
def generate_random_problems(count, file):
    """Simple program that generates COUNT random problems of a problem set described by FILE."""
    chapters = file.read().splitlines()

    problems = (
        seq(chapters)
        .map(lambda chapter: chapter.split(": ", 1))
        .map(lambda chapter: [chapter[0], string_range_to_list(chapter[1])])
        .map(
            lambda chapter: [
                chapter[0],
                seq(chapter[1]).map(lambda problem: f"{chapter[0]} #{problem}"),
            ]
        )
        .map(lambda chapter: chapter[1])
        .flatten()
        .to_list()
    )

    if count > len(problems):
        raise click.BadOptionUsage(
            option_name="count",
            message=f"{count} is greater than the maximum valid value {len(problems)}, "
            f"the number of problems described by {file.name}",
        )
    random_problem_set = random.sample(problems, count)
    for idx, problem in enumerate(random_problem_set):
        click.echo(f"{ordinal(idx + 1)} problem: {problem}")
    return random_problem_set


if __name__ == "__main__":
    generate_random_problems()
