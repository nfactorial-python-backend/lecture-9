from attrs import define
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))


@define
class ItemCreate:
    title: str
    description: str
    owner_id: int


class ItemsRepository:
    def get_item(self, db: Session, item_id: int) -> Item:
        return db.query(Item).filter(Item.id == item_id).first()

    def get_item_by_title(self, db: Session, title: str) -> Item:
        return db.query(Item).filter(Item.title == title).first()

    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
        return db.query(Item).offset(skip).limit(limit).all()

    def create_item(self, db: Session, item: ItemCreate) -> Item:
        db_item = Item(
            title=item.title,
            description=item.description,
            owner_id=item.owner_id,
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
