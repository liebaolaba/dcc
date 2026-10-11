import re
import os
import sys
import shutil
import subprocess
from androguard.core.bytecodes import apk

def apkxmlapp(apksn):
    apkstd = apk.APK(apksn)
    parse = apkstd.get_android_manifest_axml().get_xml()
    pamin = apkstd.get_main_activity()
    com = re.compile(r".*?<application.*?(android:name=|name=)\"(?P<liction>.*?)\".*?<activity.*?", re.S)
    csd = com.finditer(str(parse))
    ls = []
    for i in csd:
        ls.append(i.group("liction"))
    if ls == []:
        return "", pamin
    return ls[0], pamin

def apkxmltion(apksn):
    pxl, kmin = apkxmlapp(apksn)
    if pxl != "":
        return pxl
    else:
        return kmin

def apksignkeysha(apksn):
    apksd = apksn
    s = subprocess.check_output(['keytool', "-printcert", "-jarfile", apksd])
    print(s)
    try:
        ss = s.decode("gb18030").encode("utf-8").decode("utf-8")
    except:
        ss = s.decode("utf-8")
    com = re.compile(r".*?SHA256: (?P<sha256>.*?)\n.*?", re.S)
    csd = com.finditer(str(ss))
    ls = []
    for i in csd:
        ls.append(i.group("sha256").replace(":", ""))
    return ls[0]

def apkrepsign(psd, keysha):
    sd = psd + "/project/jni/nc/Dex2C.cpp"
    sg = psd + "/project/fcpy/Dex2C.cpp"
    sgc = psd + "/project/fcpy/Dex2C-pt.cpp"
    kg = "const char* alipy_key_sign_laba_storg="
    lign = kg + "\"" + keysha + "\"" + ";" + "\n"

    with open(sg, "r+", encoding="utf-8") as fs, open(sgc, "w", encoding="utf-8") as fd:
        number = 0
        for i in fs:
            number+=1
            if number == 10:
                i = lign
            fd.write(i)
    shutil.move(sgc, sd)

def apkdcc(psd, apksn):
    apksd = apksn[0:-4] + "-dcc.apk"
    dcc = psd + "\\dcc.py"
    subprocess.run(["python", dcc, apksn, "-o", apksd])
    return apksd

def dccpz(psd):
    pzf = "\\project-source.zip"
    pz = psd + pzf
    if os.path.exists(pz):
        prz = psd + "\\app" + pzf

        # shutil.move(pz, prz)

        return prz

def isapk(apksn):
    return apksn.endswith('.apk')

def main(apksn):
    try:
        if os.path.exists(apksn):
            if isapk(apksn):
                psd = "\\".join(os.path.abspath(__file__).split("\\")[0:-1])
                an = apksn.split("\\")[-1]
                ap = psd + "\\app\\" + an
                shutil.move(apksn, ap)
                sg = apksignkeysha(ap)
                apkrepsign(psd, sg)
                apkapcli = apkxmltion(apksn)
                apkst = "\\smali\\" + apkapcli.replace(".", "\\") + ".smali"
                with open(psd + "\\project\\fcpy\\writmin.txt", "w") as xm:
                    xm.write(apkst)

                adc = apkdcc(psd, ap)

                # 移位置
                prz = dccpz(psd)

                if os.path.exists(adc):
                    return adc
                else:
                    print("Dex2c fail")
                    os.remove(prz)
                    shutil.move(ap, apksn)
        else:
            print("failed apk")
        return None
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    apksn = sys.argv[1]
    ret = main(apksn)

    if ret:
        print(ret)
