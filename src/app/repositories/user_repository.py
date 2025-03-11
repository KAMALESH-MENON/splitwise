from typing import Optional
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.data_models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository class for handling user-related database operations.
    """

    def get(self, id: UUID) -> Optional[User]:
        """
        Retrieve a user by ID.

        Parameters:
            id (UUID): The unique identifier of the user.

        Returns:
            User | None: The user record if found, else None.
        """
        return self.session.query(User).filter(User.id == id).first()

    def get_all(
        self,
        id: UUID = None,
        name: str = None,
        phone: str = None,
        created_at: str = None,
        sort_by: str = None,
        order: str = "asc",
    ) -> list[User]:
        """
        Retrieve all users or filter by ID,name,time of creation

        Parameters:
            id (UUID, optional): Filter by user ID.
            name (str, optional): Filter by user name.
            phone (str,optional): Filter by phone
            created_at(str,optional):Filter by time of creation
            sort_by (str, optional): Column name to sort by.
            order (str, optional): Sorting order ('asc' or 'desc'). Defaults to 'asc'.

        Returns:
            List[User]: A list of user records.
        """
        users = self.session.query(User).all()

        if id:
            users = self.session.query(User).filter(User.id == id)

        if name:
            users = self.session.query(User).filter(User.name == name)

        if phone:
            users = self.session.query(User).filter(User.phone == phone)

        if created_at:
            users = self.session.query(User).filter(User.created_at == created_at)

        if sort_by:
            if hasattr(User, sort_by):
                column = getattr(User, sort_by)
                users = self.session.query(User).order_by(
                    desc(column) if order.lower() == "desc" else column
                )

        return users

    def add(self, **kwargs) -> User:
        """
        Add a new user to the database.

        Parameters:
            kwargs: Key value pairs of the attributes to update
        """
        user = User(**kwargs)
        return self.session.add(user)

    def update(self, id: UUID, **kwargs) -> None:
        """
        Update user details.

        Parameters:
            id (UUID): The unique identifier of the user to update.
            **kwargs: Key-value pairs of attributes to update.
        """
        existing_user = self.get(id=id)
        if existing_user:
            for key, value in kwargs.items():
                setattr(existing_user, key, value)

    def delete(self, id: UUID) -> None:
        """
        Delete a user by ID.

        Parameters:
            id (UUID): The unique identifier of the user.

        """
        group = self.get(id)

        if group:
            self.session.delete(group)
