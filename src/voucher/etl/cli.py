import click


@click.group()
def cli():
    pass


@cli.command()
def extract():
    pass


@cli.command()
def preprocess():
    pass


@cli.command()
def load():
    pass


if __name__ == "__main__":
    cli()
