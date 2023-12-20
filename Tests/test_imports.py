import subprocess
import unittest


class TestDataMapper(unittest.TestCase):
    def setUp(self):
        cmd = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "grep -PzL '(from|import)\sCvPythonExtensions' Assets/Python/**/*.py",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cmd_2 = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                r"grep -Pzl 'try:\n\s+(from|import)\sCvPythonExtensions' Assets/Python/**/*.py",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.outputs = cmd.communicate()[0] + cmd_2.communicate()[0]
        self.outputs = list(
            map(lambda x: x.split("/")[-1].split(".py")[0], self.outputs.splitlines())  # type: ignore
        )
        self.outputs.remove("Province")
        self.outputs = sorted(self.outputs)

    def test_imports(self):
        print("\n")
        print("\n".join(o for o in self.outputs))
        for output in self.outputs:
            __import__(output)  # type: ignore
        print("")


if __name__ == "__main__":
    unittest.main()
