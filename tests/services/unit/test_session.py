import unittest
import unittest.mock
from dto.user import UserRole
from services.session import SessionService


class TestSessionService(unittest.TestCase):
    def setUp(self):
        self.session_service = SessionService()

    def test_set_user(self):
        mock_user = unittest.mock.MagicMock()
        self.session_service.set_user(mock_user)
        self.assertEqual(self.session_service.current_user, mock_user)

    def test_clear(self):
        mock_user = unittest.mock.MagicMock()
        self.session_service.set_user(mock_user)
        self.session_service.clear()
        self.assertIsNone(self.session_service.current_user)

    def test_is_admin_with_admin_user(self):
        mock_user = unittest.mock.MagicMock()
        mock_user.type = UserRole.ADMIN.value
        self.session_service.set_user(mock_user)
        self.assertTrue(self.session_service.is_admin())

    def test_is_admin_with_non_admin_user(self):
        mock_user = unittest.mock.MagicMock()
        mock_user.type = UserRole.USER.value
        self.session_service.set_user(mock_user)
        self.assertFalse(self.session_service.is_admin())

    def test_is_admin_with_no_user(self):
        self.session_service.clear()
        self.assertFalse(self.session_service.is_admin())

    def test_is_authorized_with_user(self):
        mock_user = unittest.mock.MagicMock()
        self.session_service.set_user(mock_user)
        self.assertTrue(self.session_service.is_authorized())

    def test_is_authorized_with_no_user(self):
        self.session_service.clear()
        self.assertFalse(self.session_service.is_authorized())
