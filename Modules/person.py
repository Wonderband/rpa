class Person:
    def __init__(self, props, values):
        for prop, value in zip(props, values):
            setattr(self, prop, value)
