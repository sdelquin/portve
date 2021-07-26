#!/usr/bin/env python

import logzero
import typer

from portve import moment, services, settings
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
    ref_date = moment.build_ref_date(ref_date, tz=settings.TARGET_TZ)
    guide = TVGuide(date=ref_date)
    guide.notify()


if __name__ == "__main__":
    app()
