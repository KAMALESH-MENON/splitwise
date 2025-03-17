from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import desc

from src.app.models.data_models import User
from src.app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository class for handling user-related database operations.
    """

    def get(
        self,
        id: Optional[UUID] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Optional[User]:
        """
        Retrieve a user by ID or email.

        Parameters:
            id (UUID, optional): The unique identifier of the user.
            email (str, optional): The email of the user.
            phone (str,optional): Filter by phone

        Returns:
            User | None: The user record if found, else None.
        """
        query = self.session.query(User)

        if id:
            return query.filter(User.id == id).first()

        if email:
            return query.filter(User.email == email).first()

        if phone:
            return query.filter(User.phone == phone).first()

        return None

    def get_all(
        self,
        name: Optional[str] = None,
        created_at: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        order: str = "asc",
    ) -> list[User]:
        """
        Retrieve all users or filter by ID,name,time of creation

        Parameters:
            name (str, optional): Filter by user name.
            created_at(datetime,optional):Filter by time of creation
            sort_by (str, optional): Column name to sort by.
            order (str, optional): Sorting order ('asc' or 'desc'). Defaults to 'asc'.

        Returns:
            List[User]: A list of user records.
        """
        query = self.session.query(User)

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        if created_at:
            query = query.filter(User.created_at == created_at)

        if sort_by and hasattr(User, sort_by):
            column = getattr(User, sort_by)
            query = query.order_by(desc(column) if order.lower() == "desc" else column)

        return query.all()

    def add(self, **kwargs: object) -> None:
        """
        Add a new user to the database.

        Parameters:
            kwargs: Key value pairs of the attributes to update
        """
        user = User(**kwargs)
        self.session.add(user)

    def update(self, id: UUID, **kwargs: object) -> None:
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
        user = self.get(id)

        if user:
            self.session.delete(user)
