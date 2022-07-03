import os

package_dir = os.path.dirname(os.path.abspath('__file__'))

data_path = os.path.join(package_dir, 'data')
host = os.getenv("host", "localhost")

db = os.getenv("db", "test")
table = os.getenv("table", "winprice-data")


