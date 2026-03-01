import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock tkinter before importing app_gui_new
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

from app_gui_new import load_model, get_strength_category

class TestAppGuiNew(unittest.TestCase):
    def test_load_model(self):
        # Model file exists, so it should load successfully
        model = load_model()
        self.assertIsNotNone(model)

    def test_get_strength_category_weak(self):
        category, color = get_strength_category(2.5)
        self.assertEqual(category, "WEAK")
        self.assertEqual(color, "green")

    def test_get_strength_category_moderate(self):
        category, color = get_strength_category(4.0)
        self.assertEqual(category, "MODERATE")
        self.assertEqual(color, "yellow")

    def test_get_strength_category_strong(self):
        category, color = get_strength_category(5.5)
        self.assertEqual(category, "STRONG")
        self.assertEqual(color, "orange")

    def test_get_strength_category_severe(self):
        category, color = get_strength_category(6.5)
        self.assertEqual(category, "SEVERE")
        self.assertEqual(color, "red")

if __name__ == '__main__':
    unittest.main()