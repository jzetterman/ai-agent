import unittest
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

class TestFunctions(unittest.TestCase):
    def test_simple(self):
        result = get_files_info("calculator", ".")
        self.assertIn("is_dir=", result)
        self.assertIn("file_size=", result)
        self.assertIn("main.py", result)
        
    def test_simple(self):
        result = get_files_info("calculator", "pkg")
        self.assertIn("is_dir=", result)
        self.assertIn("file_size=", result)
        self.assertIn("calculator.py", result)

    def test_simple(self):
        result = get_files_info("calculator", "/bin")
        self.assertIn("Error: Cannot list \"/bin\" as it is outside the permitted working directory", result)

    def test_simple(self):
        result = get_files_info("calculator", "../")
        self.assertIn("Error: Cannot list \"calculator/../\" as it is outside the permitted working directory", result)


if __name__ == "__main__":
    print(run_python_file("calculator", "main.py"))
    print('##############################################')
    print(run_python_file("calculator", "tests.py"))
    print('##############################################')
    print(run_python_file("calculator", "../main.py"))
    print('##############################################')
    print(run_python_file("calculator", "nonexistent.py"))

    unittest.main()