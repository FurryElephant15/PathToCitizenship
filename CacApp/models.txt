import sqlalchemy as sa
import sqlalchemy.orm as so
from CacApp.__init__ import db
from werkzeug.security import generate_password_hash, check_password_hash


class user(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128), index = True, unique = True)
    passwords: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    house: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    senator1: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    senator2: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    president: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    vp: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    governor: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    fed_rep: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    native_language: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)


    def password_create(self, password):
        self.passwords=generate_password_hash(password)
    def password_check(self, password):
        if password == self.passwords:
            return True
        else:
            return False
