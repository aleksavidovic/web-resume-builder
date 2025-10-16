import pytest
from resume_builder.resume_builder_core.services import BasicInfoService
from resume_builder.models import BasicInfo

from resume_builder import db
import uuid

def test_create_basic_info(test_app, new_user):
    """
    GIVEN a BasicInfoService
    WHEN the 'create_basic_info' method is called
    THEN it should create a new BasicInfo object in the database
    """
    with test_app.app_context():
        service = BasicInfoService(db.session)
        basic_info_data = {
            "entry_title": "Test Entry",
            "full_name": "Test User",
            "job_title": "Tester",
            "address": "123 Test St",
            "contact_email": "test@example.com",
            "contact_phone": "1234567890",
            "linkedin_url": "linkedin.com/test",
            "github_url": "github.com/test"
        }
        service.create_basic_info(new_user.id, basic_info_data)
        
        basic_info = BasicInfo.query.filter_by(entry_title="Test Entry").first()
        assert basic_info is not None
        assert basic_info.full_name == "Test User"
        assert basic_info.user_id == new_user.id

def test_create_basic_info_missing_required_field_raises_exception(test_app, new_user):
    """
    GIVEN a BasicInfoService
    WHEN the 'create_basic_info' method is called with invalid email address
    THEN it should throw an error
    """
    with test_app.app_context():
        service = BasicInfoService(db.session)
        basic_info_data = {
            "full_name": "Test User",
            "job_title": "Tester",
            "address": "123 Test St",
            "contact_email": "invalid_email_value",
            "contact_phone": "1234567890",
            "linkedin_url": "linkedin.com/test",
            "github_url": "github.com/test"
        }
        with pytest.raises(KeyError):
            created_basic_info = service.create_basic_info(new_user.id, basic_info_data)
         
def test_create_basic_info_missing_optional_field_success(test_app, new_user):
    with test_app.app_context():
        service = BasicInfoService(db.session)
