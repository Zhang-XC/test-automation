import os
import shutil

import pytest

from common.settings import DIR_REPORT, FILE_PATH


if __name__ == "__main__":
    pytest.main(
        ["-s", "-v", f"--alluredir={DIR_REPORT}", ".", "--clean-alluredir",
            f"--junitxml={FILE_PATH['JUNIT_XML']}"])

    shutil.copy(FILE_PATH["ENV_XML"], DIR_REPORT)
    os.system(f"allure serve {DIR_REPORT}")