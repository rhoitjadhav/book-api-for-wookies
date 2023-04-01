# Packages
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

# Modules
from db.postgresql_db import Base


class BooksModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    cover_image: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    author: Mapped[str] = mapped_column(ForeignKey("users.author_pseudonym"))
    users: Mapped["UsersModel"] = relationship(back_populates="books")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
