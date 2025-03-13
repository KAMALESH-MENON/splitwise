from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import desc

from src.app.models.data_models import Group
from src.app.repositories.base_repository import BaseRepository


class GroupRepository(BaseRepository[Group]):
    """A repository class for managing Group objects in the database."""

    def get(self, id: UUID) -> Optional[Group]:
        """
        Retrieve a single Group by its UUID.

        Parameters:
            id : UUID
                The unique identifier of the group.

        Returns:
            Optional[Group]: The Group object if found, otherwise None.
        """
        group = self.session.query(Group).filter(Group.id == id).first()

        return group

    def get_all(
        self,
        id: Optional[UUID] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        created_by: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        order: str = "asc",
    ) -> list[Group]:
        """
        Retrieve all groups with optional filtering and sorting.

        Parameters:
            id (Optional[UUID]): Filter by group ID.
            name (Optional[str]): Filter by group name.
            type (Optional[str]): Filter by group type.
            created_by (Optional[UUID]): Filter by creator's UUID.
            created_at (Optional[datetime]): Filter by creation date.
            sort_by (Optional[str]): Column name to sort results by.
            order (str): Sort order, either "asc" (ascending) or "desc" (descending). Default is "asc".

        Returns:
            list[Group]: A list of Group objects matching the filters.
        """
        query = self.session.query(Group)

        if id:
            query = query.filter(Group.id == id)

        if name:
            query = query.filter(Group.name == name)

        if type:
            query = query.filter(Group.type == type)

        if created_by:
            query = query.filter(Group.created_by == created_by)

        if created_at:
            query = query.filter(Group.created_at == created_at)

        if sort_by and hasattr(Group, sort_by):
            column = getattr(Group, sort_by)
            query = query.order_by(desc(column) if order.lower() == "desc" else column)

        return query.all()

    def add(self, **kwargs: object) -> None:
        """
        Add a new Group to the database.

        Parameters:
            **kwargs (object): Key-value pairs of the attributes for the new group.
        """
        group = Group(**kwargs)
        self.session.add(group)

    def update(self, id: UUID, **kwargs: object) -> None:
        """
        Update Group details.

        Parameters:
            id (UUID): The unique identifier of the group to update.
            **kwargs (object): Key-value pairs of the attributes to update.
        """
        group = self.get(id)

        if group:
            for key, value in kwargs.items():
                setattr(group, key, value)

    def delete(self, id: UUID) -> None:
        """
        Delete a Group from the database.

        Parameters:
            id (UUID): The unique identifier of the group to delete.
        """
        group = self.get(id)

        if group:
            self.session.delete(group)
