from typing_extensions import Annotated
from typing import List, Optional, cast
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import mapped_column, relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import String, ForeignKey, Enum, DateTime
from datetime import datetime, timezone
from dependencies.custom_enum import StatusList

# ЗА ИНДЕКС УЗНАТь

class Base(MappedAsDataclass, DeclarativeBase):
    pass  

str50 = Annotated[str, 50]
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
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str50]
    max_loading: Mapped[int]
    current_loading: Mapped[int] = mapped_column(default=0)
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
    
    @hybrid_property 
    def is_active(self) -> bool:
        return self.active
    
    @is_active.expression
    def is_active_expr(cls) -> ColumnElement[bool]:
        return cast(ColumnElement[bool], cls.active)
    
    @hybrid_property
    def is_available(self) -> bool:
        return self.current_loading < self.max_loading
    
    @is_available.expression
    def is_available_expr(self) -> ColumnElement[bool]:
        return cast(ColumnElement[bool], self.current_loading < self.max_loading)
    
    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False
    
    def can_delete(self) -> bool:
        active_statuses = (StatusList.IN_PROGRESS, StatusList.NEW)
        has_active_contact = any(
            contact.status in active_statuses 
            for contact in self.contacts
        )
        return not has_active_contact
    
    def get_priority_source(self, source_id: int) -> Optional[int]:
        return next(
            (
                priority.weight 
                for priority in self.priorities 
                if priority.source_id == source_id
            ), 
            None
        )
    
    def increment_current_loading(self):
        self.current_loading += 1
    
    def decrement_current_loading(self):
        self.current_loading -= 1
    
    @validates("max_loading")
    def validate_max_loading(self, key, max_loading):
        if max_loading <= 0:
            raise ValueError("max_loading must be greater than 0")
        
        if self.current_loading is not None and max_loading < self.current_loading:
            raise ValueError("max_loading must be greater than current loading")
        return max_loading
    
    @validates("current_loading")
    def validate_current_loading(self, key, current_loading):
        if current_loading < 0:
            raise ValueError("current_loading can't be less than 0")
        
        if self.max_loading is not None and current_loading > self.max_loading:
            raise ValueError("current_loading must be less than max loading")
        return current_loading
    
    __table_args__ = (
        Index("ix_operator_active", "active"),
    )
    
    def __repr__(self):
        return f"Operator(id={self.id}, name='{self.name}', loading={self.current_loading}/{self.max_loading})"
    
class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    external_id: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        doc="Идентификатор внешней системы"
    )
    created_at: Mapped[date_created] = mapped_column(init=False)
    name: Mapped[str50] = mapped_column(nullable=True, default=None)
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan",
        order_by="Contact.created_at",
        lazy="selectin",
        doc="Контакты связанные с лидом",
        default_factory=list,
    )
    sources: Mapped[List["Source"]] = relationship(
        back_populates="leads",
        secondary="leads_sources",
        order_by="LeadsSources.created_at",
        lazy="selectin",
        doc="Источники связанные с лидом",
        default_factory=list,
    )
    
    def __repr__(self):
        return f"Lead(id={self.id}, external_id='{self.external_id}')"
    
    
class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str50]
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        order_by="Contact.created_at",
        lazy="selectin",
        doc="Контакты связанные с источником",
        default_factory=list
    )
    leads: Mapped[List["Lead"]] = relationship(
        back_populates="sources",
        secondary="leads_sources",
        order_by="LeadsSources.created_at",
        lazy="selectin",
        doc="Лиды связанные с источником",
        default_factory=list
    )
    priorities: Mapped[List["OperatorSourcePriority"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        order_by="OperatorSourcePriority.weight",
        lazy="selectin",
        doc="Приоритеты источника",
        default_factory=list
    )
    
    def can_delete(self) -> bool:
        active_statuses = (StatusList.IN_PROGRESS, StatusList.NEW)
        has_active_contact = any(
            contact.status in active_statuses 
            for contact in self.contacts
        )
        return not has_active_contact
    
    def __repr__(self):
        return f"Source(id={self.id}, name='{self.name}')"

class LeadsSources(Base):
    __tablename__ = "leads_sources"
    lead_id: Mapped[int] = mapped_column(
        ForeignKey(
            "leads.id",
            name="fk_leads_sources_lead_id"
        ),
        primary_key=True
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sources.id",
            name="fk_leads_sources_source_id"
        ),
        primary_key=True 
    )
    created_at: Mapped[date_created] = mapped_column(init=False)
    
    
class OperatorSourcePriority(Base):
    # operator_id + source_id должны быть уникальны в рамках таблицы
    __tablename__ = "operator_source_priorities"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    operator_id: Mapped[int] = mapped_column(
        ForeignKey(
            "operators.id",
            name="fk_priorities_operator_id"
        ) 
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sources.id",
            name="fk_priorities_source_id"
        ) 
    )
    weight: Mapped[int]
    operator: Mapped["Operator"] = relationship(back_populates="priorities", init=False)
    source: Mapped["Source"] = relationship(back_populates="priorities", init=False)
    created_at: Mapped[date_created] =  mapped_column(init=False)
    updated_at: Mapped[date_updated] =  mapped_column(init=False)
    
    def __repr__(self):
        return f"OperatorSourcePriority(id={self.id}, operator_id='{self.operator_id}', \
               "f"source_id='{self.source_id}', weight='{self.weight}')"
    
    __table_args__ = (
        UniqueConstraint(
            "operator_id", 
            "source_id", 
            name="uq_operator_source"
        ),
        Index("ix_operator_source_priority_operator_id", "operator_id")
    )

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    operator_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "operators.id",
            name="fk_contacts_operator_id"
        ),  
        nullable=True
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sources.id", 
            name="fk_contacts_source_id"
        ) 
    )
    lead_id: Mapped[int] = mapped_column(
        ForeignKey(
            "leads.id",
            name="fk_contacts_lead_id"
        ) 
    )
    lead: Mapped["Lead"] = relationship(back_populates="contacts", init=False)
    operator: Mapped[Optional["Operator"]] = relationship(back_populates="contacts", init=False)
    source: Mapped["Source"] = relationship(back_populates="contacts", init=False)
    created_at: Mapped[date_created] = mapped_column(init=False)
    updated_at: Mapped[date_updated] = mapped_column(init=False)
    status: Mapped[StatusList] = mapped_column(
        Enum(StatusList, name="contact_status"),
        default=StatusList.IN_QUEUE,
        doc="Статус контакта"
    )
    
    __table_args__ = (
        Index("ix_contact_operator_id", "operator_id"),
        Index("ix_contact_created_at", "created_at"),
        Index("ix_contact_status", "status")
    )
    
    def __repr__(self):
        return f"Contact(id={self.id}, operator_id='{self.operator_id}', source_id='{self.source_id}', " \
               f"lead_id='{self.lead_id}', status='{self.status}', created_at='{self.created_at}')"