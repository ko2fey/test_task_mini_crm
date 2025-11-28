from typing_extensions import Annotated
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, MappedAsDataclass
from sqlalchemy import String, ForeignKey, Enum, DateTime
import enum 
from datetime import datetime, timezone

# ЗА ИНДЕКС УЗНАТь
class StatusList(enum.Enum):
    IN_QUENUE = "in_quenue"
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Base(MappedAsDataclass, DeclarativeBase):
    pass  

str50 = Annotated[str, 50]
pk = Annotated[int, mapped_column(primary_key=True)]
op_fk = Annotated[int, mapped_column(ForeignKey("operators.id"))]
src_fk = Annotated[int, mapped_column(ForeignKey("sources.id"))]
lead_fk = Annotated[int, mapped_column(ForeignKey("leads.id"))]
date_created = Annotated[
    datetime, 
    mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        doc="Дата создания"
    )
]
date_updated = Annotated[
    datetime, 
    mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc),
        doc="Дата обновления"
    )
]

class Operator(Base):
    __tablename__ = "operators"
    id: Mapped[pk] = mapped_column(init=False)
    name: Mapped[str50]
    max_loading: Mapped[int]
    current_leads: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)
    priorities: Mapped[List["OperatorSourcePriority"]] = relationship(
        back_populates="operator",
        cascade="all, delete-orphan",
        order_by="OperatorSourcePriority.weight",
        lazy="selectin",
        doc="Приоритеты оператора",
        default_factory=list,
    )
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="operator",
        cascade="all, delete-orphan",
        order_by="Contact.created_at",
        lazy="selectin",
        doc="Контакты назначенные оператору",
        default_factory=list
    )

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[pk] = mapped_column(init=False)
    name: Mapped[str50]
    external_id: Mapped[str] = mapped_column(String(50), unique=True, doc="Идентификатор внешней системы")
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan",
        order_by="Contact.created_at",
        lazy="selectin",
        doc="Контакты связанные с лидом"
    )
    created_at: Mapped[date_created]


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[pk] = mapped_column(init=False)
    name: Mapped[str50]
    priorities: Mapped[List["OperatorSourcePriority"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        order_by="OperatorSourcePriority.weight",
        lazy="selectin",
        doc="Приоритеты источника"
    )
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        order_by="Contact.created_at",
        lazy="selectin",
        doc="Контакты связанные с источником"
    )
    

class OperatorSourcePriority(Base):
    __tablename__ = "operator_source_priorities"
    id: Mapped[pk] = mapped_column(init=False)
    operator_id: Mapped[op_fk]
    source_id: Mapped[src_fk]
    weight: Mapped[int]
    operator: Mapped["Operator"] = relationship(back_populates="priorities")
    source: Mapped["Source"] = relationship(back_populates="priorities")
    created_at: Mapped[date_created]
    updated_at: Mapped[date_updated]


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[pk] = mapped_column(init=False)
    operator_id: Mapped[Optional[op_fk]]
    source_id: Mapped[src_fk]
    lead_id: Mapped[lead_fk]
    lead: Mapped["Lead"] = relationship(back_populates="contacts")
    operator: Mapped[Optional["Operator"]] = relationship(back_populates="contacts")
    source: Mapped["Source"] = relationship(back_populates="contacts")
    created_at: Mapped[date_created]
    updated_at: Mapped[date_updated]
    status: Mapped[StatusList] = mapped_column(Enum(StatusList), default=StatusList.IN_QUENUE, doc="Статус контакта")