from abc import ABC
from sqlalchemy.orm import Session
from src.app.config.database import get_db
from src.app.repositories.user_repository import UserRepository
from fastapi import Depends


class BaseUnitOfWork(ABC):
    """A base class implementing the Unit of Work pattern for managing database transactions."""

    def __init__(self, session_factory=get_db):
        """
        Initialize the Unit of Work with a session factory.

        Parameters:
            session_factory: A function that provides a new database session.
        """
        self.session_factory = session_factory

    def __enter__(self):
        """
        Enter the runtime context, initializing a new database session.
        """
        self.session = next(self.session_factory())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context, handling transaction commit or rollback.

        Parameters:
            exc_type: Exception type if an error occurred.
            exc_value: Exception instance if an error occurred.
            traceback: Traceback object if an error occurred.
        """
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.session.close()

    def commit(self):
        """
        Commit the current transaction, persisting changes to the database.
        """
        self.session.commit()

    def rollback(self):
        """
        Roll back the current transaction, reverting uncommitted changes.
        """
        self.session.rollback()

class UserUnitOfWork(BaseUnitOfWork):
    """Unit of Work class for managing user-related transactions."""

    def __init__(self, db):
        self.session = db  
        self.user_repository = UserRepository(self.session) 

    def __enter__(self):
        """Enter the runtime context, returning itself."""
        return self

def get_user_uow(db: Session = Depends(get_db)) -> UserUnitOfWork:
    return UserUnitOfWork(db)   