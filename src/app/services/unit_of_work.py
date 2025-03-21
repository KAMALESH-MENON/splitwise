from abc import ABC

from src.app.config.database import get_db
from src.app.models.data_models import Activity, Expense, Group


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


class ExpenseUnitOfWork(BaseUnitOfWork):
    """A Unit of Work class for managing expense-related database transactions."""

    def add_expense(self, expense: Expense):
        """
        Add an expense to the database.

        Parameters:
            expense (Expense): The expense object to add.
        """
        self.session.add(expense)
        super().commit()
        self.session.refresh(expense)


class GroupUnitOfWork(BaseUnitOfWork):
    """A Unit of Work class for managing group-related database transactions."""

    def add_group(self, group: Group):
        """
        Add a group to the database.

        Parameters:
            group (Group): The group object to add.
        """
        self.session.add(group)
        super().commit()
        self.session.refresh(group)
