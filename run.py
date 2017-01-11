from server import app
from server.scripts.redisloader import load_unlabeled_into_redis
import click

@click.group()
def cli():
    pass

@cli.command()
def load_redis():
    load_unlabeled_into_redis()

if __name__ == '__main__':
    cli()
