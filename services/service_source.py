from repositories.repo_source import SourceRepository
from services.service_base import BaseService
from models import Source

class SourceService(BaseService[SourceRepository, Source]):
    def __init__(self, repository: SourceRepository) -> None:
        super().__init__(repo=repository)
