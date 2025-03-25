from abc import ABC

from src.app.config.database import get_db
from src.app.models.data_models import Activity
from src.app.repositories.expense_repository import ExpenseRepository
from src.app.repositories.group_repository import GroupRepository
from src.app.repositories.user_repository import UserRepository


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


class ExpenseUnitOfWork(BaseUnitOfWork):
    """Unit of Work for managing expense-related database transactions."""

    def __enter__(self):
        super().__enter__()
        self.expense = ExpenseRepository(session=self.session)
        self.user = UserRepository(session=self.session)
        self.group = GroupRepository(session=self.session)
        return self


class ActivityUnitOfWork(BaseUnitOfWork):
    """A Unit of Work class for managing activity-related database transactions."""

    def log_activity(self, user_id: str, group_id: str, description: str):
        """
        Log an activity in the database.

        Parameters:
            user_id (str): The ID of the user associated with the activity.
            group_id (str): The ID of the group associated with the activity.
            description (str): The description of the activity.
        """
        activity = Activity(user_id=user_id, group_id=group_id, description=description)
        self.session.add(activity)
        super().commit()
        self.session.refresh(activity)
