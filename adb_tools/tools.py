import os
import time
import subprocess
from collections import Counter
import shutil
import re


def install_and_open(device_name, file_path):
    # 安装app
    subprocess.call("tidevice --udid " + device_name + " install " + file_path)


def package_info(device_name):
    # 获取设备的具体信息
    subprocess.call(f"tidevice --udid {device_name} info")


def collect_pref(device_name, package_name, perf_index):
    # 采集性能
    if perf_index == '请选择需要关注的性能指标,不选择代表关注全部指标':
        subprocess.call(f"tidevice --udid {device_name} perf -B {package_name}")
    else:
        subprocess.call(f"tidevice --udid {device_name} perf -o {perf_index} -B {package_name}")


def close_pref(device_name):
    # 关闭采集
    res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
    for i in str(res).split(r'\n'):
        if device_name in i:
            pid = re.findall(r'(\d+)', i)[-1]
            subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
            print('采集性能服务停止！')


def kill_process(device_name, package_name):
    # 强制杀死app
    subprocess.call(f"tidevice --udid {device_name} kill {package_name}")


def get_activity(device_name):
    # 获取设备已安装应用
    print(f"设备{device_name}已安装应用：")
    subprocess.call(f"tidevice --udid {device_name} applist")


def launch_app(device_name, package_name):
    subprocess.call(f'tidevice --udid {device_name} launch {package_name}')


def screenshot(device_name):
    # 手机截图
    if not os.path.exists("D:/ios_screenshot"):
        os.mkdir("D:/ios_screenshot")
    image = f'{str(time.strftime("%Y%m%d%H%M%S", time.localtime()))}_{device_name}.png'
    subprocess.call(f"tidevice --udid {device_name} screenshot D:/ios_screenshot/{image}")


def check_process(device_name, package_name):
    # 查看进程
    if package_name == '' or package_name == '请选择app的包名':
        subprocess.call(f'tidevice --udid {device_name} ps')
    else:
        print(f"设备{device_name}的应用{package_name}当前进程信息：")
        subprocess.call(f"tidevice --udid {device_name} ps | findstr {package_name}", shell=True)


def output_log(device_name):
    # 导出缓存日志
    if not os.path.exists("D:/ios_log"):
        os.mkdir("D:/ios_log")
    log_name = f'{str(time.strftime("%Y%m%d%H%M%S", time.localtime()))}_{device_name}.txt'
    subprocess.call(f"tidevice --udid {device_name} syslog > D:/ios_log/{log_name}", shell=True)
    print(f"设备{device_name}的日志保存在D:/ios_log目录的{log_name}")


def close_output_log(device_name):
    # 关闭日志输出
    res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
    for i in str(res).split(r'\n'):
        if device_name in i:
            pid = re.findall(r'(\d+)', i)[-1]
            subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
            print('日志导出服务停止！,请在D:/ios_log查看')


def uninstall_all(device_name, package_name):
    # 卸载app
    subprocess.call("tidevice --udid " + device_name + " uninstall " + package_name)


def get_device_list():
    res = subprocess.check_output("tidevice list")
    try:
        device_list = [i.split()[0] for i in res.decode('gbk').strip().split('\n')[1:]]
        return device_list
    except IndexError:
        return []


def show_package():
    packages = []
    device_list = get_device_list()
    for i in device_list:
        res = subprocess.check_output(f"tidevice --udid {i} applist")
        packages_list = res.decode('gbk').split('\n')[:-1]
        for j in packages_list:
            packages.append(j)
    c = dict(Counter(packages))
    return [i for i in c.keys() if c[i] == len(device_list)]


def export_crash(device_name):
    if not os.path.exists("D:/ios_log"):
        os.mkdir("D:/ios_log")
        if not os.path.exists(f'D:/ios_log/{device_name}'):
            os.mkdir(f"D:/ios_log/{device_name}")
    subprocess.call(f'tidevice --udid {device_name} crashreport --keep D:/ios_log/{device_name}')
    today = str(time.strftime("%Y-%m-%d-%H%M", time.localtime()))
    crash_list = os.listdir(f'D:/ios_log/{device_name}')
    for i in crash_list:
        if os.path.isfile(f'D:/ios_log/{device_name}/{i}'):
            if today not in i:
                os.remove(f'D:/ios_log/{device_name}/{i}')
        else:
            shutil.rmtree(f'D:/ios_log/{device_name}/{i}')
    print(f'设备{device_name}导出的崩溃日志保存在D:/ios_log/{device_name}')
