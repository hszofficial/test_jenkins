from pathlib import Path
PROJECT_PATH = Path(__file__).absolute().parent.parent
TEST_PATH = PROJECT_PATH.joinpath("test")
TEST_DB_URL = "sqlite:///user.db"#"postgresql://postgres:postgres@localhost:5432/test"
TEMPLATE_PATH = str(PROJECT_PATH.joinpath("templates"))
STATIC_FOLDER = str(PROJECT_PATH.joinpath("static"))
