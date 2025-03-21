from datetime import datetime

from ..models.data_models import Group, GroupUser
from ..schemas.schemas import GroupSchema
from ..services.unit_of_work import ActivityUnitOfWork, GroupUnitOfWork


def create_group(
    uow: GroupUnitOfWork,
    activity_uow: ActivityUnitOfWork,
    user_id: str,
    group_name: str,
):
    """
    Create a new group and log the activity.
    """
    with uow:
        group = Group(
            name=group_name, type="other", created_by=user_id, created_at=datetime.now()
        )
        uow.add_group(group)
        uow.session.refresh(group)

        group_id = group.id

        group_data = GroupSchema.from_orm(group)

    with activity_uow:
        activity_uow.log_activity(user_id, group_id, f"Created group '{group_name}'")

    return group_data
