
import subprocess,re, random
import pexpect, time
class fingerprintsetter(object):
    def __init__(self):
        print('')


    def commands(self):

        cmd2 = f'adb shell getprop ro.build.fingerprint'
        result = subprocess.Popen(cmd2,shell=True, stdout=subprocess.PIPE).stdout.read()
        if type(result) == type(bytes()):
            result = result.decode()
        print(result)

        
        c1 = 'adb shell props'

        child = pexpect.spawn(c1)
        time.sleep(2)
        child.sendline('1')

        time.sleep(2)
        child.sendline('f')
        time.sleep(2)
        child.sendline('27')
        time.sleep(2)
        child.sendline('1')
        time.sleep(2)
        child.sendline('y')
        time.sleep(2)
        child.sendline('y')
        time.sleep(2)
        for i in range(200):
            rb = child.readline(size=i).decode()
            print(rb)
            if 'Rebooting' in rb:
                break
            #print()


    def create_sh(self):
        with open('good_records.txt','r') as f:
            fingerprints = f.read().split('\n')
            f.close()

        while True:
            fp = random.choice(fingerprints)
            print(fp)
            android_version = re.findall('\((\d+)\)',fp)
            print(android_version)
            if len(android_version) == 0:
                continue
            else:
                android_version = android_version[0]
            if int(android_version) >= 9:
                break
        print(fp)
        rf = f'''PRINTSLIST="
        {fp}
        "
        BASICATTMODEL="SM-A300FU"'''.replace('        ','')
        with open('Samsung.sh','w') as f:
            f.write(rf)
            f.close()

    def push_sh(self):
        cmd = f'adb push Samsung.sh /sdcard/Download/Samsung.sh'
        subprocess.Popen(cmd,shell=True)

        # find the location for Magisk 
        cmd2 = f'adb shell  su -c "find -name \\\"MagiskHidePropsConf\\\" -print | head -n 1"'
        result = subprocess.Popen(cmd2,shell=True, stdout=subprocess.PIPE).stdout.read()
        if type(result) == type(bytes()):
            result = result.decode()
        print(result)
        res_path = re.findall('\.(\/dev.*)',result)[0]
        print(res_path)
        cmd3 = f'adb shell su -c "cp /sdcard/Download/Samsung.sh {res_path}/printfiles/Samsung.sh"'
        subprocess.Popen(cmd3,shell=True)
        time.sleep(2)
        cmd4 = f'adb shell su -c "cat {res_path}/printfiles/Samsung.sh"'
        result = subprocess.Popen(cmd4,shell=True, stdout=subprocess.PIPE).stdout.read()
        if type(result) == type(bytes()):
            result = result.decode()
        print(result)        


if __name__ == "__main__":
    fps = fingerprintsetter()
    #fps.commands()
    fps.create_sh()
    #raise 'eee'
    fps.push_sh()
    fps.commands()
