import os
import sys

if __name__ == "__main__":
    # apkp = sys.argv[1]
    ds = "\\".join(os.path.abspath(__file__).split("\\")[0:-1])
    dsc = "cd " + ds

    # apkp = ds + "\\app\\" + "lacolvideo.apk"

    apkp = ds + "\\app\\" + "app_s.apk"

    # apkp = ds + "\\app\\" + "svc.apk"

    dcl = "python dccloader.py " + apkp
    os.system(dsc)
    os.system(dcl)
