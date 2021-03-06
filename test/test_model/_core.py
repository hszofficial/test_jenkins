import sys
import unittest
from pathlib import Path
try:
    from test.const import PROJECT_PATH, TEST_PATH, TEST_DB_URL
except:
    test_dir = str(Path(__file__).absolute().parent.parent)

    if test_dir not in sys.path:
        sys.path.append(test_dir)
    from const import PROJECT_PATH, TEST_PATH, TEST_DB_URL

src_path = str(PROJECT_PATH.joinpath("test_drone"))

if src_path not in sys.path:
    sys.path.append(src_path)
from model import (
    bind_db,
    drop_tables,
    get_table,
    moke_data
)


class Core(unittest.TestCase):
    # 初始化数据库和连接
    @classmethod
    def setUpClass(cls):
        print("setUp model test context")

    @classmethod
    def tearDownClass(cls):
        print("tearDown model test context")

    def setUp(self):
        print("create test db")
        bind_db(TEST_DB_URL)
        moke_data()
        print("instance setUp")

    def tearDown(self):
        print("delete test db")
        drop_tables()
        print("instance tearDown")

    def get_table(self, table_name):
        return get_table(table_name)
