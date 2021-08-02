#!/usr/bin/env python

import logzero
import typer

from portve import services
from portve.core import TVGuide

app = typer.Typer(add_completion=False)
logger = services.init_logger()


@app.command()
def notify(
    verbose: bool = typer.Option(False, '--verbose', '-vv', show_default=False),
    ref_date: str = typer.Option('today', '--ref_date', help='today or tomorrow'),
):
    '''Notify TVGuide to Telegram Channel based on indicated search terms'''
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)
    guide = TVGuide(ref_date=ref_date)
    guide.notify()


if __name__ == "__main__":
    app()
