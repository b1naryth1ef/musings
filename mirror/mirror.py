import os, json, time

THREE_HOURS = 60 * 60 * 3

MIRRORS = {}

if not os.path.exists(".cache"):
    os.mkdir(".cache")

for dirpath, dirname, files in os.walk("mirrors"):
    for fname in files:
        if fname.endswith(".json"):
            data = json.load(open(os.path.join(dirpath, fname), "r"))
            MIRRORS[fname.rsplit(".", 1)[0]] = data

HEAD = os.getcwd()
while True:
    for mirror in MIRRORS:
        cdir = os.path.join(".cache", mirror)
        if not os.path.exists(cdir):
            os.mkdir(cdir)
            print ("git clone {} {}".format(
                MIRRORS[mirror]["remote"],
                cdir))
            os.popen("git clone {} {}".format(
                MIRRORS[mirror]["remote"],
                cdir))
            os.chdir(cdir)
            os.popen("git remote add mirror {}".format(
                MIRRORS[mirror]["mirror"]))
            os.popen("git push -u mirror master")
            os.chdir(HEAD)
        else:
            os.chdir(cdir)
            os.popen("git fetch")
            os.popen("git pull --all")
            os.popen("git push --all mirror")
            os.popen("git push --tags mirror master")
            os.chdir(HEAD)
    time.sleep(THREE_HOURS)
