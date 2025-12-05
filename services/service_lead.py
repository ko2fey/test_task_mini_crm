from models import Lead, Contact
from repositories.repo_lead import LeadRepository
from typing import Optional, List

class LeadService:
    def __init__(self, lead_repository):
        self.repo: LeadRepository = lead_repository
        
    def get_contacts(self, id: int):
        contacts = self.repo.get_list_contacts(id)
        response = {
            'objects': contacts,
            'total_count': len(contacts)
        }
        return response