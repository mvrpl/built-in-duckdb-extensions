from importlib.resources import files
import duckdb

_EXT_ROOT = files(__name__) / "_extensions"

config = {
    "autoinstall_known_extensions": False,
    "allow_unsigned_extensions": True,
    "extension_directories": [_EXT_ROOT.as_posix()],
}

con = duckdb.connect(":memory:", config=config)

con.load_extension("aws")
con.load_extension("iceberg")