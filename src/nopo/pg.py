class Pg:
    """Base page. You can build your own page based on it."""

    def __init__(self, drv):
        self.driver = drv