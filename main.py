"""2022/3 HUJI OOP generic test file , created by Daniel Nachum
(see version bellow)

To run edit details in the section marked as "Edit"
and then just run normally with an IDE or from the terminal
"""
import urllib.request
import urllib.parse
import urllib
import os
import platform
# ============================== EDIT =========================================
# ==== Test Execution ====
FILES: "list[tuple[str, str, list[str], list[tuple], list[tuple]]]" = [
    [
        "java",  # executer
        "Chat",  # executable
        [],  # args - maybe not working, I haven't checked
        [  # inputs
            ["hi", 5],
            ["hello", 3]
        ],
        [  # outputs
            [""],
            [""]
        ]
    ],
]
# ================================= DONT TOUCH BELOW ====================================


VERSION = 1
VERSION_URL = "https://github.com/danielnachumdev/HUJI-OOP-tests/blob/main/ex1/version"
PIP = ".\\venv\\Scripts\\pip.exe"
PYTHON_NAME = {
    "Windows": "python",
    "Darwin": "python3",  # Darwin => Mac
    "Linux": "python3"
}[platform.system()]
PYTHON = f".\\venv\\Scripts\\{PYTHON_NAME}.exe"
TMPFILE = ".\\__TEMP_TEST_FILE__.py"
# check if python is running in wsl
if 'microsoft-standard' in platform.uname().release:
    raise RuntimeWarning(
        "test.py is still not configured properly for wsl, you are welcome to fix it and send a pull request")
    PIP = "./venv/bin/pip"
    PYTHON = f"./venv/bin/{PYTHON_NAME}"
    TMPFILE = TMPFILE.replace("\\", "/")


def cm(cm: str) -> str:
    """execute simple command in terminal

    Args:
        cm (str): command input

    Returns:
        str: result of command
    """
    return os.popen(cm).read()


def setup():
    """perform setup for test execution
    """
    def update():
        def check_for_update() -> bool:
            def get_html(url: str) -> str:
                user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
                headers = {'User-Agent': user_agent, }
                req = urllib.request.Request(url, headers=headers)
                html = urllib.request.urlopen(req).read().decode('UTF-8')
                return html

            def original_to_raw_url(url: str):
                return url.replace("github.com", "raw.githubusercontent.com").replace("blob/", "")

            version_as_string = get_html(original_to_raw_url(VERSION_URL))

            def is_update_needed(current_version: str, online_version: str) -> bool:
                curr_numbers = current_version.split(".")
                online_numbers = online_version.split(".")
                for i in range(min(len(curr_numbers), len(online_numbers))):
                    if int(curr_numbers[i]) < int(online_numbers[i]):
                        return True
                return len(curr_numbers) < len(online_numbers)

            return is_update_needed(str(VERSION), version_as_string)

        print("checking for update...", end="")
        if check_for_update():
            print("\na newer version exists")
            print(
                f"visit https://github.com/danielnachumdev/HUJI-OOP-tests/tree/main/ex1 for newer version")
        else:
            print("ok")

    def install():
        def directory_exists(path: str) -> bool:
            return os.path.exists(path) and os.path.isdir(path)

        if not directory_exists("./venv"):
            print("first time setup")
            print("creating venv")
            cm(f"{PYTHON_NAME} -m venv venv")
            print("updating venv")
            cm(f"{PYTHON} -m pip install --upgrade pip > nul 2>&1")
        print("\033[0m", end="")
        print("checking dependencies...", end="")
        if "danielutils" not in [v.split(" ")[0] for v in cm(f"{PIP} list").split("\n")]:
            print("\ninstalling dependencies to venv")
            print(cm(f"{PIP} --quiet install danielutils > nul 2>&1"))
        else:
            print("ok")
    update()
    install()


def test():
    """
    """
    def write_to_file(path: str, lines) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def get_code(executer: str, executable: str, args: list, inputs: list, outputs: list) -> str:
        cases = []

        def wrap(value) -> str:
            if isinstance(value, str):
                return f"\"{value}\""
            return str(value)

        for input, output in zip(inputs, outputs):
            input = ", ".join(wrap(v) for v in input)
            output = ", ".join(wrap(v) for v in output)
            cases.append(f"\t\tTest([{input}],[{output}])")
        test_string = ",\n".join(cases)
        command = " ".join([executer, executable]+args)
        return \
            f"""import sys
from danielutils import TestFactory, Test, acm, bytes_to_str
def main():
    def inner(user_word: str, amount_of_enter_presses: int):
        return_code, stdout, stderr = acm(command=f\"{command}\",inputs=[user_word]+["" for _ in range (amount_of_enter_presses)],i_timeout=0.01)
        return bytes_to_str(stdout)
        
    TestFactory(inner, verbose=True).add_tests([
{test_string}
    ])()

if __name__ == "__main__":
    main()
    """

    print("beginning testing")
    for executer, executable, args, inputs, outputs in FILES:
        lines = [f"{v}\n" for v in get_code(
            executer, executable, args, inputs, outputs).split("\n")]
        write_to_file(TMPFILE, lines)
        print(cm(f"{PYTHON} {TMPFILE}"))
        os.remove(TMPFILE)


def main():
    setup()
    test()


if __name__ == "__main__":
    main()
