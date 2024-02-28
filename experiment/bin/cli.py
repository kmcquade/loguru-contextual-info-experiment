import click
from experiment.commands.scan import scan
from experiment.bin.logger import init_logger


@click.group()
@click.option("--env", "environment_name", type=str, help="The environment name.", required=False)
def cli(environment_name):
    init_logger(environment_name)


cli.add_command(scan)


def main():
    cli()


if __name__ == '__main__':
    main()
