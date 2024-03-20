#!/usr/bin/python3
"""
Unit test cases for the HBNBCommand console.
"""
import unittest
import models
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """ Unittests for the HBNB console """
    
    def setUp(self):
        """ Setting up the HBNBCommand instance for testing """
        self.console = HBNBCommand()

    def test_create_command(self):
        """ Testing the create command """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create("User")
            output = fake_out.getvalue().strip()
            # Check if output contains the ID of the created instance
            self.assertTrue(output.startswith("u-"))
            # Check if the created instance exists in storage
            self.assertIn(output, models.storage.all())

    def test_show_command(self):
        """ Testing the show command """
        user = models.User()
        user.save()
        # Run show command for the test user instance
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_show("User {}".format(user.id))
            output = fake_out.getvalue().strip()
            # Check if output contains information about the user
            self.assertIn(str(user), output)

    def test_destroy_command(self):
        """ Testing the destroy command """
        user = models.User()
        user.save()
        # Run destroy command for the test user instance
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_destroy("User {}".format(user.id))
            # Check if the user instance is removed from storage
            self.assertNotIn(user.id, models.storage.all())

    def test_all_command(self):
        """ Testing the all command """
        user = models.User()
        user.save()
        place = models.Place()
        place.save()
        # Run all command
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_all("")
            output = fake_out.getvalue().strip()
            # Check if output contains information about all objects
            self.assertIn(str(user), output)
            self.assertIn(str(place), output)
        # Run all command for specific class
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_all("User")
            output = fake_out.getvalue().strip()
            # Check if output contains information about objects of User class
            self.assertIn(str(user), output)
            self.assertNotIn(str(place), output)

    def test_count_command(self):
        """ Testing the count command """
        user1 = models.User()
        user1.save()
        user2 = models.User()
        user2.save()
        place1 = models.Place()
        place1.save()
        # Run count command for User class
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_count("User")
            output = fake_out.getvalue().strip()
            # Check if output contains correct count of User instances
            self.assertEqual(output, "2")

    def test_update_command(self):
        """ Testing the update command """
        user = models.User()
        user.save()
        # Run update command to update attribute of the user instance
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_update("User {} email \"test@example.com\"".format(user.id))
            # Check if the user instance's attribute is updated
            self.assertEqual(user.email, "test@example.com")


if __name__ == "__main__":
    unittest.main()
