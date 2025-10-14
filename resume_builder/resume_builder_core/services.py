from ..models import BasicInfo
from .exceptions import AuthorizationError, EntryNotFoundError

class BasicInfoService:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_basic_info(self, user_id: str, new_basic_info_data: dict):
        try:
            new_basic_info = BasicInfo()
            new_basic_info.entry_title = new_basic_info_data["entry_title"].data
            new_basic_info.full_name = new_basic_info_data["full_name"].data
            new_basic_info.job_title = new_basic_info_data["job_title"].data
            new_basic_info.address = new_basic_info_data["address"].data
            new_basic_info.contact_email = new_basic_info_data["contact_email"].data
            new_basic_info.contact_phone = new_basic_info_data["contact_phone"].data
            new_basic_info.linkedin_url = new_basic_info_data["linkedin_url"].data
            new_basic_info.github_url = new_basic_info_data["github_url"].data
            new_basic_info.user_id = user_id
            self.db_session.add(new_basic_info)
            self.db_session.commit()
        except Exception as e:
            raise e

    def get_basic_info_by_id(self, user_id: str, entry_id: str) -> BasicInfo:
        basic_info = BasicInfo.query.filter_by(id=entry_id).first()
        if not basic_info:
            raise EntryNotFoundError("No Basic Info entry found for provided id.")
        if basic_info.user_id != user_id:
            raise AuthorizationError("You are not authorized to view this entry.")
        return basic_info

    def get_basic_infos_by_user_id(self, user_id: str) -> list[BasicInfo] | None:
        basic_infos = BasicInfo.query.filter_by(user_id=user_id).all()
        return basic_infos

    def update_basic_info(self, user_id: str, entry_id: str, updated_basic_info_data: dict):
        basic_info_to_update = BasicInfo.query.filter_by(id=entry_id).first()
        if not basic_info_to_update:
            raise EntryNotFoundError("No basic info entry for provided id")
        if basic_info_to_update.user_id != user_id:
            raise AuthorizationError("You are not authorized to modify this entry.")
        basic_info_to_update.entry_title = updated_basic_info_data["entry_title"].data
        basic_info_to_update.full_name = updated_basic_info_data["full_name"].data
        basic_info_to_update.job_title = updated_basic_info_data["job_title"].data
        basic_info_to_update.address = updated_basic_info_data["address"].data
        basic_info_to_update.contact_email = updated_basic_info_data["contact_email"].data
        basic_info_to_update.contact_phone = updated_basic_info_data["contact_phone"].data
        basic_info_to_update.linkedin_url = updated_basic_info_data["linkedin_url"].data
        basic_info_to_update.github_url = updated_basic_info_data["github_url"].data
        self.db_session.commit()
        return basic_info_to_update

    def delete_basic_info_by_id(self, user_id:str, basic_info_id: str) -> None:
        basic_info_to_delete = BasicInfo.query.filter_by(id=basic_info_id).first()
        if not basic_info_to_delete:
            raise EntryNotFoundError("No basic info entry for provided id")
        self.db_session.delete(basic_info_to_delete)
        self.db_session.commit()
