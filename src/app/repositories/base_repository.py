from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[T]:
        return NotImplementedError()

    @abstractmethod
    def get_all(self) -> List[T]:
        return NotImplementedError()

    @abstractmethod
    def add(self, **kwargs: object) -> None:
        return NotImplementedError()

    @abstractmethod
    def update(self, id: UUID, **kwargs: object) -> None:
        return NotImplementedError()

    @abstractmethod
    def delete(self, id: UUID) -> None:
        return NotImplementedError()
