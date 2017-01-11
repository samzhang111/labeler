from server.app import app
from server.scripts.redisloader import load_unlabeled_into_redis
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--count', default=10000, help='Number of IDs to load into redis')
def load_redis(count):
    load_unlabeled_into_redis(count)
    click.echo('Done')

if __name__ == '__main__':
    cli()
