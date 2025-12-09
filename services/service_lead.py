from models import Lead
from repositories.repo_lead import LeadRepository
from services.service_base import BaseService

class LeadService(BaseService[LeadRepository, Lead]):
    def __init__(self, lead_repository):
        self.repo: LeadRepository = lead_repository
        
    def get_sources(self, id: int):
        sources = self.repo.get_list_sources(id)
        response = {
            'objects': sources,
            'total_count': len(sources)
        }
        print(response)
        return response