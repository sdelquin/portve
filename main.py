#!/usr/bin/env python

import logzero
import typer

from portve import moment, services
from portve.core import TVGuide

app = typer.Typer(add_completion=False)
logger = services.init_logger()


@app.command()
def notify(ref_date: str = typer.Option('today', '--ref_date', help='today or tomorrow')):
    '''Notify TVGuide to Telegram Channel based on indicated search terms'''
    ref_date = moment.build_ref_date(ref_date)
    guide = TVGuide(date=ref_date)
    guide.notify()


@app.callback()
def main(verbose: bool = False):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)


if __name__ == "__main__":
    app()
