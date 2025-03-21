from .unit_of_work import ActivityUnitOfWork


def log_activity(
    uow: ActivityUnitOfWork, user_id: str, group_id: str, description: str
):
    """
    Log an activity in the database.
    """
    with uow:
        uow.log_activity(user_id, group_id, description)
