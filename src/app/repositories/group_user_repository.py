from datetime import datetime
from typing import List, Optional
from uuid import UUID 
from .base_repository import BaseRepository
from ..models.data_models import GroupUser


class GroupUserRepository(BaseRepository[GroupUser]):
    """
    Repository for managing GroupUser entities.
    Provides methods for retrieving, adding, updating, and deleting GroupUser records.
    """

    def get(self, id: UUID) -> Optional[GroupUser]:
        """
        Retrieve a GroupUser by its unique ID.

        Args:
            id (UUID): The unique identifier of the GroupUser.

        Returns:
            Optional[GroupUser]: The corresponding GroupUser instance if found, otherwise None.
        """
        return self.session.query(GroupUser).filter(GroupUser.id == id).first()

    def get_all(
        self,
        group_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        joined_at: Optional[datetime] = None,
        sort_by: Optional[str] = None
    ) -> List[GroupUser]:
        """
        Retrieve all GroupUser records with optional filters and sorting.

        Args:
            group_id (Optional[UUID]): If provided, filters results by group ID.
            user_id (Optional[UUID]): If provided, filters results by user ID.
            joined_at (Optional[datetime]): If provided, filters results by the exact join date.
            sort_by (Optional[str]): If provided, sorts results by the specified attribute.

        Returns:
            List[GroupUser]: A list of GroupUser instances matching the filters.
        """
        query = self.session.query(GroupUser)

        if group_id:
            query = query.filter(GroupUser.group_id == group_id)

        if user_id:
            query = query.filter(GroupUser.user_id == user_id)

        if joined_at:
            query = query.filter(GroupUser.joined_at == joined_at)

        if group_id and user_id:
            query = query.filter(GroupUser.group_id == group_id, GroupUser.user_id == user_id)

        if sort_by:
            query = query.order_by(getattr(GroupUser, sort_by))

        return query.all()

    def add(self, **kwargs: object) -> None:
        """
        Add a new GroupUser record to the database.

        Args:
            **kwargs (object): Keyword arguments representing the attributes of the new GroupUser instance.
        
        Returns:
            None
        """
        group_user = GroupUser(**kwargs)
        self.session.add(group_user)

    def update(self, id: UUID, **kwargs: object) -> None:
        """
        Update an existing GroupUser record.

        Args:
            id (UUID): The unique identifier of the GroupUser to update.
            **kwargs (object): The attributes to update with their new values.

        Returns:
            None
        """
        group_user = self.get(id=id)
        if group_user:
            for key, value in kwargs.items():
                setattr(group_user, key, value)

    def delete(self, id: UUID) -> None:
        """
        Delete a GroupUser record from the database.

        Args:
            id (UUID): The unique identifier of the GroupUser to delete.

        Returns:
            None
        """
        group_user = self.get(id=id)
        if group_user:
            self.session.delete(group_user)
