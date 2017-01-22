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

@cli.command()
def run():
    click.echo('Running:')
    app.run()
    click.echo('Done')

@cli.command()
def list_routes():
    from pprint import pprint
    pprint(app.url_map)

if __name__ == '__main__':
    cli()
