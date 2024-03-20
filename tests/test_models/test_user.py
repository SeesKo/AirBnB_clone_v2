#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        cls.user = User()

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)

    def test_inheritance(self):
        """Test inheritance from BaseModel"""
        self.assertTrue(issubclass(User, BaseModel))

    def test_attributes(self):
        """Test class attributes"""
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'password'))
        self.assertTrue(hasattr(self.user, 'first_name'))
        self.assertTrue(hasattr(self.user, 'last_name'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "Not applicable")
    def test_attributes_file_storage(self):
        """Test attributes for file storage"""
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Not applicable")
    def test_attributes_db_storage(self):
        """Test attributes for database storage"""
        self.assertTrue(isinstance(self.user.email, str))
        self.assertTrue(isinstance(self.user.password, str))
        self.assertTrue(isinstance(self.user.first_name, str))
        self.assertTrue(isinstance(self.user.last_name, str))

    def test_user_creation(self):
        """Test user instance creation"""
        self.assertTrue(isinstance(self.user, User))

    def test_first_name_type(self):
        """Test type of first_name attribute"""
        self.assertIsInstance(self.user.first_name, str)

    def test_last_name_type(self):
        """Test type of last_name attribute"""
        self.assertIsInstance(self.user.last_name, str)

    def test_email_type(self):
        """Test type of email attribute"""
        self.assertIsInstance(self.user.email, str)

    def test_password_type(self):
        """Test type of password attribute"""
        self.assertIsInstance(self.user.password, str)

    def test_str_representation(self):
        """Test __str__ method"""
        string = str(self.user)
        self.assertTrue("[User]" in string)
        self.assertTrue("id" in string)
        self.assertTrue("created_at" in string)
        self.assertTrue("updated_at" in string)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print(self, mock_stdout):
        """Test print method"""
        expected_output = "[User] ({}) {}\n".format(
            self.user.id, self.user.__dict__)
        print(self.user)
        self.assertEqual(mock_stdout.getvalue(), expected_output)
