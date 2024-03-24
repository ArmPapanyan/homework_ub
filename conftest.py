import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    return checkout(f'mkdir {data["FOLDER_TST"]} {data["FOLDER_OUT"]} {data["FOLDER_1"]} {data["FOLDER_2"]}',  "")

@pytest.fixture()
def clear_folders():
    return checkout(f'rm -rf {data["FOLDER_TST"]} {data["FOLDER_OUT"]} {data["FOLDER_1"]} {data["FOLDER_2"]}',  "")

@pytest.fixture()
def make_files():
    list_off_files = [ ]
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data["FOLDER_TST"]}; dd if=/dev/urandom of=file{i} bs={data["SIZE"]} count=1 iflag=fullblock', ""):
            list_off_files.append(f'filename{i}')
    return list_off_files

@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["FOLDER_TST"], subfoldername), ""):
        return None, None
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["FOLDER_TST"], subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/arxbad -t{}".format(data["FOLDER_TST"], data["FOLDER_OUT"], data["type"]), "Everything is Ok")
    checkout("truncate -s 1 {}/arxbad.{}".format(data["FOLDER_OUT"], data["type"]), "Everything is Ok")
    yield "arxbad"
    checkout("rm -f {}/arxbad.{}".format(data["FOLDER_OUT"], data["type"]), "")

@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "")