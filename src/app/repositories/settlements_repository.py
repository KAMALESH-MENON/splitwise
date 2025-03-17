from typing import List, Optional
from uuid import UUID
from sqlalchemy import desc
from src.app.models.data_models import Settlements
from repositories.base_repository import BaseRepository


class SettlementRepository(BaseRepository[Settlements]):
    """
    Repository class for handling settlement-related database operations.

    This class provides methods to retrieve, filter, add, update, and delete settlements
    while supporting dynamic filtering and sorting options.
    """

    def get(self, id: UUID) -> Settlements:
        """
        Fetch a settlement by its unique ID.

        param id: UUID of the settlement to retrieve.
        return: The Settlement object if found, else None.
        """

        return self.session.query(Settlements).filter(Settlements.id == id).first()

    def get_all(
        self,
        payer_id: Optional[UUID] = None,
        payee_id: Optional[UUID] = None,
        expense_split_id: Optional[UUID] = None,
        is_settled: Optional[bool] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
    ) -> List[Settlements]:
        """
        Fetch all settlements with optional filtering and sorting.

        param payer_id: (Optional) UUID of the payer to filter settlements.
        param payee_id: (Optional) UUID of the payee to filter settlements.
        param expense_split_id: (Optional) UUID of the associated expense split.
        param is_settled: (Optional) Boolean to filter settlements by their status.
        param sort_by: (Optional) Field name to sort results (e.g., 'created_at').
        param order: (Optional) Sorting order, "asc" (default) or "desc".
        return: A list of settlements matching the filters.
        """
        query = self.session.query(Settlements)
        if payer_id:
            query = query.filter(Settlements.payer_id == payer_id)
        if payee_id:
            query = query.filter(Settlements.payee_id == payee_id)
        if expense_split_id:
            query = query.filter(Settlements.expense_split_id == expense_split_id)
        if is_settled is not None:
            query = query.filter(Settlements.is_settled == is_settled)

        if sort_by and hasattr(Settlements, sort_by):
            column = getattr(Settlements, sort_by)
            query = query.order_by(desc(column) if order.lower() == "desc" else column)

        return query.all()

    def add(self, **kwargs: object) -> None:
        """
        Add a new settlement to the database.

        param kwargs: Dictionary of settlement attributes (e.g., payer_id, payee_id, amount).
        return: None
        """

        settlement = Settlements(**kwargs)
        self.session.add(settlement)

    def update(self, id: UUID, **kwargs: object) -> None:
        """
        Update an existing settlement in the database.

        param id: UUID of the settlement to update.
        param kwargs: Dictionary of fields to update.
        return: None
        """

        settlement = self.get(id)
        if settlement:
            for key, value in kwargs.items():
                setattr(settlement, key, value)

    def delete(self, id: UUID) -> None:
        """
        Delete a settlement by its unique ID.

        param id: UUID of the settlement to delete.
        return: None
        """

        settlement = self.get(id)
        if settlement:
            self.session.delete(settlement)
