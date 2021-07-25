#!/usr/bin/env python

import typer

from portve import services
from portve.core import TVGuide

app = typer.Typer()


@app.command()
def notify(ref_date: str = typer.Option('today', '--ref_date', help='today or tomorrow')):
    ref_date = services.build_ref_date(ref_date)
    guide = TVGuide(date=ref_date)
    guide.notify()


if __name__ == "__main__":
    app()
