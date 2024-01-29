from src.lib.repository import SQLAlchemyRepository
from src.models import Encounter

class EncounterRepository(SQLAlchemyRepository):
    model = Encounter