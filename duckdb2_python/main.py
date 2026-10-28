from importlib.resources import files
import duckdb
import os

_EXT_ROOT = files(__name__) / "_extensions"

config = {
    "autoinstall_known_extensions": False,
    "allow_unsigned_extensions": True,
    "extension_directories": [_EXT_ROOT.as_posix()],
}

def main():
    con = duckdb.connect(":memory:", config=config)

    con.load_extension("aws")
    con.load_extension("iceberg")
    con.load_extension("postgres")
    con.load_extension("mysql")

    con.execute("""
    CREATE OR REPLACE SECRET aws_secret (
        TYPE s3,
        PROVIDER credential_chain,
        REGION 'sa-east-1'
    );
    """)

    con.execute(f"""
    ATTACH IF NOT EXISTS '{os.environ['AWS_ACCOUNT']}' AS glue_catalog (
        TYPE ICEBERG,
        ENDPOINT_TYPE 'glue',
        SECRET aws_secret
    );
    """)

    print(con.sql("SELECT * FROM glue_catalog.teste.tabela_telefones;"))

    con.close()