from __future__ import annotations

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .db.models.base import Base

cors = CORS()
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
