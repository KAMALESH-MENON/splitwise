from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, desc

from src.app.models.data_models import Expense
from src.app.repositories.base_repository import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):
    """
    A repository class for Expense model.
    It provides methods to perform CRUD operations on Expense data.
    """

    def get_all(
        self,
        group_id: Optional[UUID] = None,
        total_amount: Optional[float] = None,
        created_at: Optional[datetime] = None,
        paid_by: Optional[UUID] = None,
        expense_type: Optional[str] = None,
        sort_by: Optional[str] = None,
        order_by: str = "asc",
        page: int = 1,
        page_size: int = 10,
    ) -> List[Expense]:
        """
        Retrieves all expenses with optional filters, sorting, and pagination.

        Parameters:
            group_id: Filter by group ID
            total_amount: Filter by total amount of an expense
            created_at: Filter by date of an expense creation
            paid_by: Filter by payer ID who paid for the total expense
            expense_type: Filter by expense type
            sort_by: Field to sort by
            order_by: Sort by order ('asc' or 'desc')
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
        List of filtered, sorted, and paginated expenses
        """

        query = self.session.query(Expense)

        if group_id:
            query = query.filter(Expense.group_id == group_id)
        if total_amount:
            query = query.filter(Expense.total_amount == total_amount)
        if created_at:
            query = query.filter(Expense.created_at == created_at)
        if paid_by:
            query = query.filter(Expense.paid_by == paid_by)
        if expense_type:
            query = query.filter(Expense.expense_type == expense_type)

        if sort_by and hasattr(Expense, sort_by):
            column = getattr(Expense, sort_by)
            query = query.order_by(column.asc() if order_by == "asc" else column.desc())

        query = query.offset((page - 1) * page_size).limit(page_size)
        return query.all()

    def get(self, id: UUID) -> Expense:
        """
        Retrieves a single expense by its ID.

        Parameter:
            id: Expense ID

        Returns:
        Expense object or None if not found
        """
        expense = self.session.query(Expense).filter(Expense.id == id).first()
        return expense

    def add(self, **kwargs) -> None:
        """
        Adds a new expense to the database.

        Parameter:
            expense: Expense object to add
            kwargs: Dictionary of fields to update
        """
        expense = Expense(**kwargs)
        self.session.add(expense)

    def update(self, id: UUID, **kwargs) -> None:
        """
        Updates an existing expense with new values.

        Parameters:
            id: Expense ID
            kwargs: Dictionary of fields to update
        """
        expense = self.get(id=id)
        if expense:
            for key, value in kwargs.items():
                setattr(expense, key, value)

    def delete_expense(self, id: UUID) -> None:
        """
        Deletes an expense from the database.

        Parameter:
            id: Expense ID
        """
        expense = self.get(id=id)

        if expense:
            self.session.delete(expense)
