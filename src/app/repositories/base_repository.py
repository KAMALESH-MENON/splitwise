from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    """
    A generic base repository that defines common CRUD operations for database entities.

    This abstract class serves as a blueprint for repository implementations,
    providing methods for retrieving, list all, adding, updating, and deleting records.

    Type Parameters:
        T (TypeVar): The entity type that the repository manages.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Parameters:
            session (Session): SQLAlchemy session used for database operations.
        """
        self.session = session

    @abstractmethod
    def get(self, id: UUID) -> Optional[T]:
        """
        Retrieve an entity by its unique identifier.

        Parameters:
            id (UUID): The unique identifier of the entity.

        Returns:
            Optional[T]: The entity if found, otherwise None.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Retrieve all entities from the database.

        Returns:
            List[T]: A list of all entities.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, **kwargs: dict) -> None:
        """
        Add a new entity to the database.

        Parameters:
            **kwargs (object): The attributes of the entity to be created.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, id: UUID, **kwargs: dict) -> None:
        """
        Update an existing entity in the database.

        Parameters:
            id (UUID): The unique identifier of the entity to be updated.
            **kwargs (dict): The keys and values to update.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """
        Delete an entity from the database by its unique identifier.

        Parameters:
            id (UUID): The unique identifier of the entity to be deleted.
        """
        raise NotImplementedError()
