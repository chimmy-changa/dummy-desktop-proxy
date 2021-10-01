# Copyright 2020-2021 The MathWorks, Inc.
import os
from setuptools.command.install import install
import setuptools
from pathlib import Path
from shutil import which
from matlab_desktop_proxy.default_config import default_config
from matlab_desktop_proxy import __version__

npm_install = ["npm", "--prefix", "gui", "install", "gui"]
npm_build = ["npm", "run", "--prefix", "gui", "build"]


class InstallNpm(install):
    def run(self):

        # Ensure npm is present
        if which("npm") is None:
            raise Exception(
                "npm must be installed and on the path during package install!"
            )

        self.spawn(npm_install)
        self.spawn(npm_build)
        target_dir = Path(self.build_lib) / self.distribution.packages[0] / "gui"
        self.mkpath(str(target_dir))
        self.copy_tree("gui/build", str(target_dir))

        # In order to be accessible in the package, turn the built gui into modules
        (Path(target_dir) / "__init__.py").touch(exist_ok=True)
        for (path, directories, filenames) in os.walk(target_dir):
            for directory in directories:
                (Path(path) / directory / "__init__.py").touch(exist_ok=True)

        super().run()


tests_require = [
    "pytest",
    "pytest-env",
    "pytest-cov",
    "pytest-mock",
    "pytest-aiohttp",
    "requests",
    "psutil",
]

HERE = Path(__file__).parent.resolve()
long_description = (HERE / "README.md").read_text()

setuptools.setup(
    name="dummy-desktop-proxy",
    version=__version__,
    url=default_config["url"],
    author="The MathWorks, Inc.",
    # TODO: Update email
    author_email="jupyter-support@mathworks.com",
    license="MATHWORKS CLOUD REFERENCE ARCHITECTURE LICENSE",
    # TODO: Update description
    description=" Python® package enables you to open a MATLAB® desktop in a web browser tab.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["devel", "tests"]),
    # TODO: keywords, classfiers.
    keywords=["Jupyter"],
    classifiers=["Framework :: Jupyter"],
    python_requires="~=3.6",
    install_requires=["aiohttp>=3.7.4"],
    tests_require=tests_require,
    extras_require={
        "dev": ["aiohttp-devtools", "black", "ruamel.yaml"] + tests_require
    },
    entry_points={
        "matlab_desktop_proxy_configs": [
            "default_config = matlab_desktop_proxy.default_config:default_config"
        ],
        "console_scripts": ["matlab-desktop-proxy-app = matlab_desktop_proxy.app:main"],
    },
    include_package_data=True,
    zip_safe=False,
    cmdclass={"install": InstallNpm},
)
