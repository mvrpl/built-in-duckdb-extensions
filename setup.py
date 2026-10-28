from pathlib import Path
from setuptools import setup
from setuptools.command.sdist import sdist

DUCKDB_VERSION = "2.0.0"

EXTENSIONS = {
    "aws": {
        "url": "http://extensions.duckdb.org",
        "sha256_linux_amd64": "f6e8b47c1f0aba8313fd571dc179ecf766c8c6c88842b04efbe54b5d9340f7bc",
        "sha256_linux_arm64": "73c715031b8e47c6e29700697d7df654517d53d9e26442b1e672d1672bfe767d"
    },
    "iceberg": {
        "url": "http://extensions.duckdb.org",
        "sha256_linux_amd64": "ddc8e8f4af60e6e3accffa1b38043c328c810db91215d6299f29cc933655bf1a",
        "sha256_linux_arm64": "dc5fc010b24a044ec2dc34294d8d251f481560cfbd5819c22f1fb1b6cc0032ae"
    },
    "avro": {
        "url": "http://extensions.duckdb.org",
        "sha256_linux_amd64": "35447cb42ade2f723f53416ee336dc9ee30ba3584f290e01165398c80f56fd92",
        "sha256_linux_arm64": "1d240802771737ae14695b9d544ecac170832f38dda9a3edcb674ee1d546c2ca"
    },
    "httpfs": {
        "url": "http://extensions.duckdb.org",
        "sha256_linux_amd64": "ee6c7d7e60a5da1b6f6bf6156b4298b55ddce0496a5bfe628bd6ab6d47eb8e3e",
        "sha256_linux_arm64": "f524888fc7d74cc0c6c4a8f7ed5beedac5b12e71cb426503f882c72ce6afbd43"
    },
    "postgres_scanner": {
        "url": "http://extensions.duckdb.org",
        "sha256_linux_amd64": "54b3d751cafc9ffa439886b1607d0ee758dab4dc070f0171e779b95f2f3e554f",
        "sha256_linux_arm64": "afe7f2bd798b61e4c2e1f96deedaa70a21d15eebc8cd9470beb923951d0ce58a"
    },
    "mysql_scanner": {
        "url": "http://extensions.duckdb.org",
        "sha256_linux_amd64": "edfc8d927178c32b740064f18f292c3fc67f62de32d6a61874fef7cca3d12591",
        "sha256_linux_arm64": "9beb65e9b2c48465f90d37f89191907c128531f770ab11e7ffb198ca94a3ed83"
    }
}

class Sdist(sdist):
    def run(self):
        for plat in ["linux_amd64", "linux_arm64"]:
            dest = Path(self.build_lib) / "mvrpl_br_pkg" / "_extensions" / f"v{DUCKDB_VERSION}" / plat
            dest.mkdir(parents=True, exist_ok=True)
            for name, meta in EXTENSIONS.items():
                url = f"{meta['url']}/v{DUCKDB_VERSION}/{plat}/{name}.duckdb_extension.gz"
                print(f"baixando {url}")
                with urllib.request.urlopen(url, timeout=120) as r:
                    raw = gzip.decompress(r.read())
                digest = hashlib.sha256(raw).hexdigest()
                if digest != meta[f'sha256_{plat}']:
                    raise RuntimeError(f"sha256 divergente para {name}: {digest}")
                (dest / f"{name}.duckdb_extension").write_bytes(raw)
        super().run()

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
    cmdclass={"sdist": Sdist}
)