from abc import ABC

from src.app.config.database import get_db
from src.app.repositories.settlements_repository import SettlementRepository


class BaseUnitOfWork(ABC):
    """A base class implementing the Unit of Work pattern for managing database transactions."""

    def __init__(self, session_factory=get_db):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = next(self.session_factory())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class PaymentUnitOfWork(BaseUnitOfWork):
    """Unit of Work for handling payment history operations."""

    def __enter__(self):
        super().__enter__()
        self.settlement_repository = SettlementRepository(self.session)
        return self
