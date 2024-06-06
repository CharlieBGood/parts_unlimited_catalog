import sqlite3
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import OperationalError

CREATION_RAW_SQL = """
    CREATE TABLE part (
        id INTEGER PRIMARY KEY,
        name VARCHAR(150),
        sku VARCHAR(30),
        description VARCHAR(1024),
        weight_ounces INTEGER,
        is_active TINYINT(1)
    );
"""

INSERTION_RAW_SQL = """
    INSERT INTO part (name, sku, description, weight_ounces, is_active)
    VALUES
    ('Heavy coil', 'SDJDDH8223DHJ', 'Tightly wound nickel-gravy alloy
    spring', 22, 1),
    ('Reverse lever', 'DCMM39823DSJD', 'Attached to provide inverse
    leverage', 9, 0),
    ('Macrochip', 'OWDD823011DJSD', 'Used for heavy-load computing', 2,
    1);
"""

class Command(BaseCommand):
    help = "Starts db with initial data"

    def handle(self, *_, **__):
        try:
            with connection.cursor() as cursor:
                cursor.execute(CREATION_RAW_SQL)
                cursor.execute(INSERTION_RAW_SQL)
                self.stdout.write(
                    self.style.SUCCESS('Successfully created db')
                )

        except (OperationalError, sqlite3.Warning) as e:
            raise CommandError(str(e))
            