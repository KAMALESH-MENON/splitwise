from src.app.services.unit_of_work import ActivityUnitOfWork


def log_activity(
    uow: ActivityUnitOfWork, user_id: str, group_id: str, description: str
):
    """
    Log an activity in the database.

    Args:
        uow (ActivityUnitOfWork): Unit of work instance to manage database operations.
        user_id (str): Unique identifier of the user performing the activity.
        group_id (str): Unique identifier of the group associated with the activity.
        description (str): Description of the activity being logged.

    Returns:
        None
    """
    with uow:
        uow.log_activity(user_id, group_id, description)
