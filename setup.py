import gzip
import sysconfig
import urllib.error
import urllib.request
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py

DUCKDB_VERSION = "2.0.0"

EXTENSIONS = {
    "aws": {
        "url": "http://extensions.duckdb.org"
    },
    "iceberg": {
        "url": "http://extensions.duckdb.org"
    },
    "avro": {
        "url": "http://extensions.duckdb.org"
    },
    "httpfs": {
        "url": "http://extensions.duckdb.org"
    },
    "postgres_scanner": {
        "url": "http://extensions.duckdb.org"
    },
    "mysql_scanner": {
        "url": "http://extensions.duckdb.org"
    }
}

def duckdb_platform() -> str:
    plat = sysconfig.get_platform()
    arm = "arm64" in plat or "aarch64" in plat
    if plat.startswith("linux"):
        return "linux_arm64" if arm else "linux_amd64"
    if plat.startswith("macosx"):
        return "osx_arm64" if arm else "osx_amd64"
    if plat.startswith("win"):
        return "windows_amd64"
    raise RuntimeError(f"Plataforma não mapeada: {plat}")

class BuildPy(build_py):
    def run(self):
        super().run()
        plat = duckdb_platform()
        dest = Path(self.build_lib) / "duckdb2_python" / "_extensions" / f"v{DUCKDB_VERSION}" / plat
        dest.mkdir(parents=True, exist_ok=True)
        for name, meta in EXTENSIONS.items():
            url = f"{meta['url']}/v{DUCKDB_VERSION}/{plat}/{name}.duckdb_extension.gz"
            req = urllib.request.Request(url, headers={"User-Agent": "python-build/0.1"})
            print(f"baixando {url}")
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = gzip.decompress(r.read())
            (dest / f"{name}.duckdb_extension").write_bytes(raw)

setup(
    name="duckdb2-python",
    version="0.1.0",
    packages=["duckdb2_python"],
    python_requires="==3.13.*",
    install_requires=[
        f"duckdb==2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.13",
    ],
    cmdclass={"build_py": BuildPy}
)