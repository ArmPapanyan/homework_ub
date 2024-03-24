from checkers import checkout, getout


FOLDER_TST = data['FOLDER_TST']
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_1 = data['FOLDER_1']
FOLDER_2 = data['FOLDER_2']
list_of_files = ["file1.txt", "file2.txt", "file3.txt"]

@pytest.fixture()
def make_folders():
    return checkout(f'mkdir {data["FOLDER_TST"]} {data["FOLDER_OUT"]} {data["FOLDER_1"]} {data["FOLDER_2"]}',  "")

@pytest.fixture()
def clear_folders:
    return checkout(f'rm -rf {data["FOLDER_TST"]} {data["FOLDER_OUT"]} {data["FOLDER_1"]} {data["FOLDER_2"]}',  "")

def test_step1():
    # test1
    res1 = checkout(f"cd {FOLDER_TST} ; 7z a {FOLDER_OUT}/arx2",  "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_OUT}", "arx2.7z")

    assert res1 and res2, "test1 FAIL"

def test_step2():
    # test2
    res1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(FOLDER_OUT, FOLDER_1), "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_1}", "test1")
    res3 = checkout(f"ls {FOLDER_1}", "test2")
    assert res1 and res2 and res3, "test2 FAIL"

def test_step3():
    # test3
    assert checkout(f"cd {FOLDER_OUT} ; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"

def test_step4():
    # test4
    assert checkout(f"cd {FOLDER_TST} ; 7z u arx2.7z", "Everything is Ok"), "test4 FAIL"



def test_step5():
    # test5
    res1 = checkout("cd {}; 7z l arx2.7z".format(FOLDER_OUT, FOLDER_1), "test1.txt")
    res2 = checkout("cd {}; 7z l arx2.7z".format(FOLDER_OUT, FOLDER_1), "test2.txt")
    assert res1 and res2, "test5 FAIL"

def test_step6():
    # test6
    res1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(FOLDER_OUT,FOLDER_1), "Everything is Ok")
    res2 = checkout("ls {}".format(FOLDER_2), "test1")
    res3 = checkout("ls {}".format(FOLDER_2), "test2")
    res4 = checkout("ls {}".format(FOLDER_2), "testfldr")
    res5 = checkout("ls {}".format(FOLDER_2), "test3")
    assert res1 and res2 and res3 and res4 and not res5, "test6 FAIL"

def test_step7():
    # test7
    assert checkout("cd {}; 7z d arx2.7z".format(FOLDER_OUT), "Everything is Ok"), "test7 FAIL"

def test_step8():
    # test8
    res1 = checkout("cd {}; 7z h test1.txt".format(FOLDER_TST), "Everything is Ok")
    hash = getout("cd {}; crc32 test1.txt".format(FOLDER_TST)).upper()
    res2 = checkout("cd {}; 7z h test1.txt".format(FOLDER_TST), hash)
    assert res1 and res2, "test8 FAIL"