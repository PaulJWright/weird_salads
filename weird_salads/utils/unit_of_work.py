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
        """
        Flow of Execution:

        - When No Exception Occurs:

            The try block completes normally, and the finally block ensures the
            session is closed. The if exc_type is not None block is skipped, as
            there’s no exception to handle.

        - When an Exception Occurs:

            The try block detects an exception (exc_type is not None)
            self.rollback() is called to revert any changes made during the
            session. The finally block executes, closing the session.
            After closing the session, the exception is re-raised with raise
            exc_val, ensuring that the caller knows about the failure.


        This approach correctly handles the transaction lifecycle, ensuring that:

        Any changes made during the transaction are rolled back if an error occurs.
        Resources (like the database session) are properly released no matter what.
        The exception is not swallowed, enabling appropriate error handling by the
        calling code.

        -----------------------------------------------------------------------
        Original Code

        def __exit__(self, exc_type, exc_val, traceback):
            if exc_type is not None:
                self.rollback()
                self.session.close()
            self.session.close()

        The original code committed changes before exceptions were detected
        because the commit() operation wasn't properly guarded by exception handling.
        The improved code fixes this by ensuring that if an exception occurs,
        it rolls back the transaction and does not commit anything to the database.
        """
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
