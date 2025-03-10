"""Test the Quizlet import functionality"""

from .base import BaseApiActionsMixin
from api_routes import Routes

class TestQuizletImport(BaseApiActionsMixin):
    """Test class for Quizlet import functionality"""

    def test_successful_quizlet_import(self):
        """Test successful import from Quizlet"""
        # Create a test user first
        token = self.create_user("test_user")
        # Create a folder for the user before importing Quizlet
        folder_creation_data = {
            "jwtToken": token,
            "folder": "test_folder"
        }
        self.post_api(Routes.ROUTE_CREATE_FOLDER["url"], folder_creation_data)
        # Test data
        test_data = {
            "jwtToken": token,
            "folder": "test_folder",
            "quizlet_url": "https://quizlet.com/686459638/test-set-flash-cards/?funnelUUID=a88312bb-e490-4f6c-a7da-1d844b694e24"
        }

        # Make the API call
        response = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)
  
        # Assert response status
        assert "success" in str(response) 

    def test_invalid_url(self):
        """Test import with invalid Quizlet URL"""
        # Create a test user
        token = self.create_user("test_user")
    
        folder_creation_data = {
                    "jwtToken": token,
                    "folder": "test_folder_new"
                }
        
        self.post_api(Routes.ROUTE_CREATE_FOLDER["url"], folder_creation_data)

        # Test data with invalid URL
        test_data = {
            "jwtToken": token,
            "folder": "test_folder_new",
            "quizlet_url": "https://invalid-url.com"
        }

        res = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)
        assert "Invalid or inaccessible Quizlet URL" in str(res)

    def test_duplicate_set_name(self):
        """Test importing same set twice (should fail on second attempt)"""
        # Create a test user
        token = self.create_user("test_user")
        print(token)

        folder_creation_data = {
                    "jwtToken": token,
                    "folder": "test_folder_new1"
                }
        
        self.post_api(Routes.ROUTE_CREATE_FOLDER["url"], folder_creation_data)


        # Test data
        test_data = {
            "jwtToken": token,
            "folder": "test_folder_new1",
            "quizlet_url": "https://quizlet.com/686459638/test-set-flash-cards/?funnelUUID=a88312bb-e490-4f6c-a7da-1d844b694e24"
        }

        # First import should succeed
        first_response = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)
        assert first_response["success"] == "Flashcards imported from Quizlet"
    
         # Second import should fail with duplicate error
        res = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)
        assert "Flashcard set name already exists" in str(res)

    def test_missing_parameters(self):
        """Test import with missing required parameters"""
        # Create a test user
        token = self.create_user("test_user")
        
        # Test data with missing URL
        test_data = {
            "jwtToken": token,
            "folder": "test_folder"
        }

        res = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)
        assert "The request should be in the format:" in  str(res)

    def test_import_to_non_existing_folder(self):
        """Test import into a non-existing folder"""
        # Create a test user
        token = self.create_user("test_user")
        
         test_data = {
            "jwtToken": token,
            "folder": "test_folder_new1",
            "quizlet_url": "https://quizlet.com/686459638/test-set-flash-cards/?funnelUUID=a88312bb-e490-4f6c-a7da-1d844b694e24"
        }

        # First import should succeed
        first_response = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)



        # Test data with a non-existing folder
        test_data = {
            "jwtToken": token,
            "folder": "non_existing_folder",
            "quizlet_url": "https://quizlet.com/686459638/test-set-flash-cards/?funnelUUID=a88312bb-e490-4f6c-a7da-1d844b694e24"
        }

        # Make the API call
        response = self.post_api(Routes.ROUTE_IMPORT_FROM_QUIZLET["url"], test_data)
        
        # Assert response indicates the folder does not exist
        assert "Folder does not exist" in str(response)
        