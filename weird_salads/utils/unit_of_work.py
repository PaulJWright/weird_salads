from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class UnitOfWork:
    def __init__(self):
        self.session_maker = sessionmaker(
            # !TODO create an environment variable
            bind=create_engine("sqlite:///data/orders.db")
        )

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        try:
            if exc_type is not None:
                self.rollback()
        finally:
            self.session.close()

        if exc_type is not None:
            raise exc_val

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
