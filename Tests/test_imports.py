import subprocess
import unittest


class TestDataMapper(unittest.TestCase):
    def setUp(self):
        cmd = subprocess.Popen(
            ["/bin/bash", "-c", "grep -L 'CvPythonExtensions' Assets/Python/**/*.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.outputs = cmd.communicate()[0]
        self.outputs = list(
            map(lambda x: x.split("/")[-1].split(".py")[0], self.outputs.splitlines())  # type: ignore
        )

    def test_imports(self):
        for output in self.outputs:
            __import__(output)  # type: ignore


if __name__ == "__main__":
    unittest.main()
