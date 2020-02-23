import click
from tcgen.generator import CardGenerator

@click.group()
def cli():
    pass

@cli.command()
def generate():
    CardGenerator().generate()
