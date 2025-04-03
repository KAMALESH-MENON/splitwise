from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """
    Represents a user in the Splitwise application.

    Attributes:
        id (UUID): The unique identifier for the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        phone (str, optional): The phone number of the user.
        profile_picture_url (str, optional): The URL of the user's profile picture.
        created_at (datetime): The timestamp when the user was created.
        groups (relationship): The groups the user is part of.
        expenses (relationship): The expenses the user has paid.
        expense_splits (relationship): The expense splits associated with the user.
        settlements_payed (relationship): The settlements the user has paid.
        settlements_received (relationship): The settlements the user has received.
    """

    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    groups = relationship("GroupUser", back_populates="user")
    expenses = relationship("Expense", back_populates="payer")
    expense_splits = relationship("ExpenseSplit", back_populates="user")
    settlements_payed = relationship(
        "Settlements", foreign_keys="Settlements.payer_id", back_populates="payer"
    )
    settlements_received = relationship(
        "Settlements", foreign_keys="Settlements.payee_id", back_populates="payee"
    )


class Group(Base):
    """
    Represents a group in the Splitwise application.

    Attributes:
        id (UUID): The unique identifier for the group.
        name (str): The name of the group.
        type (str): The type of the group (trip, home, other).
        created_by (UUID): The user who created the group.
        created_at (datetime): The timestamp when the group was created.
        users (relationship): The users who are part of the group.
        expenses (relationship): The expenses associated with the group.
    """

    __tablename__ = "groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum("trip", "home", "other", name="group_type"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    users = relationship("GroupUser", back_populates="group")
    expenses = relationship("Expense", back_populates="group")


class GroupUser(Base):
    """
    Represents the association between a user and a group.

    Attributes:
        id (UUID): The unique identifier for the association.
        group_id (UUID): The unique identifier for the group.
        user_id (UUID): The unique identifier for the user.
        joined_at (datetime): The timestamp when the user joined the group.
        group (relationship): The group associated with the user.
        user (relationship): The user associated with the group.
    """

    __tablename__ = "group_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.now(timezone.utc))
    group = relationship("Group", back_populates="users")
    user = relationship("User", back_populates="groups")


class Expense(Base):
    """
    Represents an expense in the Splitwise application.

    Attributes:
        id (UUID): The unique identifier for the expense.
        group_id (UUID, optional): The unique identifier for the group associated with the expense.
        total_amount (Float): The total amount of the expense.
        description (str, optional): The description of the expense.
        expense_type (str): The type of the expense (GROUP, NON-EXPENSE GROUP).
        paid_by (UUID): The user who paid the expense.
        created_at (datetime): The timestamp when the expense was created.
        updated_at (datetime): The timestamp when the expense was last updated.
        group (relationship): The group associated with the expense.
        payer (relationship): The user who paid the expense.
        splits (relationship): The splits associated with the expense.
    """

    __tablename__ = "expenses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    total_amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    expense_type = Column(
        Enum("GROUP", "NON-EXPENSE GROUP", name="expense_type_enum"), nullable=False
    )
    paid_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime, default=datetime.now(timezone.utc), onupdate=func.now(), nullable=True
    )
    group = relationship("Group", back_populates="expenses")
    payer = relationship("User", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")


class ExpenseSplit(Base):
    """
    Represents a split of an expense in the Splitwise application.

    Attributes:
        id (UUID): The unique identifier for the expense split.
        expense_id (UUID): The unique identifier for the expense.
        user_id (UUID): The unique identifier for the user.
        amount_owed (Float): The amount owed by the user.
        split_type (str): The type of the split (UNEQUALLY, EQUALLY, BY SHARES, BY PERCENTAGE, BY ADJUSTMENTS).
        updated_at (datetime): The timestamp when the split was last updated.
        expense (relationship): The expense associated with the split.
        user (relationship): The user associated with the split.
        settlements (relationship): The settlements associated with the split.
    """

    __tablename__ = "expense_splits"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    expense_id = Column(UUID(as_uuid=True), ForeignKey("expenses.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount_owed = Column(Float, nullable=False)
    split_type = Column(
        Enum(
            "UNEQUALLY",
            "EQUALLY",
            "BY SHARES",
            "BY PERCENTAGE",
            "BY ADJUSTMENTS",
            name="split_type_enum",
        ),
        nullable=False,
    )
    updated_at = Column(
        DateTime, default=datetime.now(timezone.utc), onupdate=func.now(), nullable=True
    )
    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")
    settlements = relationship("Settlements", back_populates="expense_split")


class Settlements(Base):
    """
    Represents a settlement of an expense split in the Splitwise application.

    Attributes:
        id (UUID): The unique identifier for the settlement.
        expense_split_id (UUID): The unique identifier for the expense split.
        payer_id (UUID): The unique identifier for the user who paid.
        payee_id (UUID): The unique identifier for the user who received the payment.
        amount (Float): The amount of the settlement.
        is_settled (bool): Whether the settlement is settled.
        created_at (datetime): The timestamp when the settlement was created.
        expense_split (relationship): The expense split associated with the settlement.
        payer (relationship): The user who paid the settlement.
        payee (relationship): The user who received the settlement.
    """

    __tablename__ = "settlements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    expense_split_id = Column(
        UUID(as_uuid=True), ForeignKey("expense_splits.id"), nullable=False
    )
    payer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    payee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    is_settled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expense_split = relationship("ExpenseSplit", back_populates="settlements")
    payer = relationship(
        "User", foreign_keys=[payer_id], back_populates="settlements_payed"
    )
    payee = relationship(
        "User", foreign_keys=[payee_id], back_populates="settlements_received"
    )
