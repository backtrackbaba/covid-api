import click


def register(app):
    @app.cli.group()
    def local():
        """Translation and localization commands."""
        pass

    @local.command()
    @click.argument('db')
    def init(db):
        """Initialize a new language."""
        print("Hello World!!!" + db)
