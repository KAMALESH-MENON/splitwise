from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, desc

from app.models.data_models import ExpenseSplit
from app.repositories.base_repository import BaseRepository


class ExpenseSplitRepository(BaseRepository[ExpenseSplit]):
    """
    Repository for managing ExpenseSplit entities.
    Provides methods for CRUD operations and querying by various filters.
    """

    def get(self, id: UUID) -> Optional[ExpenseSplit]:
        """
        Retrieve an ExpenseSplit by its ID.

        :parameter id: UUID of the ExpenseSplit
        :return: ExpenseSplit object or None if not found
        """
        return self.session.query(ExpenseSplit).filter(ExpenseSplit.id == id).first()

    def get_all(
        self,
        id: Optional[UUID] = None,
        amount_owed: Optional[float] = None,
        split_type: Optional[str] = None,
        user_id: Optional[UUID] = None,
        expense_id: Optional[UUID] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
    ) -> List[ExpenseSplit]:
        """
        Retrieve all ExpenseSplits matching the given filters.

        :parameter id: UUID of the ExpenseSplit
        :parameter amount_owed: Amount owed in the ExpenseSplit
        :parameter split_type: Type of split
        :parameter user_id: UUID of the user
        :parameter expense_id: UUID of the expense
        :parameter sort_by: Field to sort by
        :parameter order: Sort order ('asc' or 'desc')
        :return: List of matching ExpenseSplit objects
        """
        query = self.session.query(ExpenseSplit)

        if id:
            query = query.filter(ExpenseSplit.id == id)
        if amount_owed:
            query = query.filter(ExpenseSplit.amount_owed == amount_owed)
        if split_type:
            query = query.filter(ExpenseSplit.split_type == split_type)
        if user_id:
            query = query.filter(ExpenseSplit.user_id == user_id)
        if expense_id:
            query = query.filter(ExpenseSplit.expense_id == expense_id)

        if sort_by:
            if order == "asc":
                query = query.order_by(asc(getattr(ExpenseSplit, sort_by)))
            else:
                query = query.order_by(desc(getattr(ExpenseSplit, sort_by)))

        return query.all()

    def add(self, **kwargs: object) -> None:
        """
        Add a new ExpenseSplit to the database.

        :parameter kwargs: Fields and values for the new ExpenseSplit
        """
        expense_split = ExpenseSplit(**kwargs)
        self.session.add(expense_split)

    def update(self, id: UUID, **kwargs: object) -> None:
        """
        Update an existing ExpenseSplit.

        :parameter id: UUID of the ExpenseSplit to update
        :parameter kwargs: Fields and values to update
        """
        expense_split = self.get(id)
        if expense_split:
            for key, value in kwargs.items():
                setattr(expense_split, key, value)

    def delete(self, id: UUID) -> None:
        """
        Delete an ExpenseSplit from the database.

        :parameter id: UUID of the ExpenseSplit to delete
        """
        expense_split = self.get(id)
        if expense_split:
            self.session.delete(expense_split)
