import datetime
from uuid import uuid4

from sqlalchemy import (
    DECIMAL,
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
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
    __tablename__ = "groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum("trip", "home", "other", name="group_type"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    users = relationship("GroupUser", back_populates="group")
    expenses = relationship("Expense", back_populates="group")


class GroupUser(Base):
    __tablename__ = "group_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    group = relationship("Group", back_populates="users")
    user = relationship("User", back_populates="groups")


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    total_amount = Column(DECIMAL, nullable=False)
    description = Column(Text, nullable=True)
    expense_type = Column(
        Enum("GROUP", "NON-EXPENSE GROUP", name="expense_type_enum"), nullable=False
    )
    paid_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    group = relationship("Group", back_populates="expenses")
    payer = relationship("User", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    expense_id = Column(UUID(as_uuid=True), ForeignKey("expenses.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount_owed = Column(DECIMAL, nullable=False)
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
    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")
    settlements = relationship("Settlements", back_populates="expense_split")


class Settlements(Base):
    __tablename__ = "settlements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    expense_split_id = Column(
        UUID(as_uuid=True), ForeignKey("expense_splits.id"), nullable=False
    )
    payer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    payee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    is_settled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    expense_split = relationship("ExpenseSplit", back_populates="settlements")
    payer = relationship(
        "User", foreign_keys=[payer_id], back_populates="settlements_payed"
    )
    payee = relationship(
        "User", foreign_keys=[payee_id], back_populates="settlements_received"
    )
