import click
from flask.cli import with_appcontext

from .database import database
from .models.clothes import Clothes


@click.command("create_all", help="Create all tables in the app's databases")
@with_appcontext
def create_all():
    database.create_all()

@click.command("drop_all", help="Drop all tables in the specified database")
@with_appcontext
def drop_all():
    database.drop_all()


@click.command("insert", help="Insert a piece of clothes in your database")
@click.argument("name", type=click.STRING)
@click.argument("min_temp", type=click.INT)
@click.argument("max_temp", type=click.INT)
@click.argument("when_rain", type=click.BOOL)
@click.argument("when_snow", type=click.BOOL)
@click.argument("when_wind", type=click.BOOL)
@click.argument("is_accessoire", type=click.BOOL)
@with_appcontext
def insert(name, min_temp, max_temp, when_rain, when_snow, when_wind ,is_accessoire):
    item = Clothes(
        name=name,
        min_temp=min_temp,
        max_temp=max_temp,
        when_rain=when_rain,
        when_snow=when_snow,
        when_wind=when_wind,
        is_accessoire=is_accessoire
    )
    database.session.add(item)
    database.session.commit()


@click.command("populate", help="Populate the database with initial data")
@with_appcontext
def populate():
    initial_clothes = [
        Clothes(
            name="t-shirt",
            min_temp=0,
            max_temp=40
        ),
        Clothes(
            name="sweater",
            min_temp=-20,
            max_temp=10
        ),
        Clothes(
            name="shirt",
            min_temp=-10,
            max_temp=20
        ),
        Clothes(
            name="raincoat",
            min_temp=0,
            max_temp=10,
            when_rain=True,
            when_wind=True
        ),
        Clothes(
            name="overcoat",
            min_temp=-5,
            max_temp=10,
            when_rain=True,
            when_wind=True
        ),
        Clothes(
            name="denim jacket",
            min_temp=10,
            max_temp=20
        ),
        Clothes(
            name="hoodie",
            min_temp=5,
            max_temp=15,
            when_wind=True
        ),
        Clothes(
            name="winter coat",
            min_temp=-20,
            max_temp=0,
            when_snow=True,
            when_wind=True
        ),
        Clothes(
            name="umbrella",
            when_rain=True,
            when_snow=False,
            when_wind=False,
            is_accessoire=True
        ),
        Clothes(
            name="gloves",
            min_temp=-20,
            max_temp=0,
            when_rain=False,
            when_snow=True,
            when_wind=False,
            is_accessoire=True
        ),
        Clothes(
            name="hat",
            when_rain=True,
            when_snow=True,
            when_wind=False,
            is_accessoire=True
        )
    ]
    for clothes in initial_clothes:
        database.session.add(clothes)
    database.session.commit()
