import threading
from adb_tools.tools import *


def install(apk_name):
    for device in get_device_list():
        threading.Thread(target=install_and_open, args=(device, apk_name)).start()


def run():
    for device in get_device_list():
        threading.Thread(target=package_info, args=(device,)).start()


def launch(package_name):
    for device in get_device_list():
        threading.Thread(target=launch_app, args=(device, package_name)).start()


def perf(package_name, pref_index):
    for device in get_device_list():
        threading.Thread(target=collect_pref, args=(device, package_name, pref_index)).start()


def off_perf():
    for device in get_device_list():
        threading.Thread(target=close_pref, args=(device,)).start()


def kill(package_name):
    for device in get_device_list():
        threading.Thread(target=kill_process, args=(device, package_name)).start()


def activity():
    for device in get_device_list():
        threading.Thread(target=get_activity, args=(device,)).start()


def screen():
    for device in get_device_list():
        threading.Thread(target=screenshot, args=(device,)).start()


def check(package_name):
    for device in get_device_list():
        threading.Thread(target=check_process, args=(device, package_name)).start()


def export():
    for device in get_device_list():
        threading.Thread(target=output_log, args=(device,)).start()


def off_output():
    for device in get_device_list():
        threading.Thread(target=close_output_log, args=(device,)).start()


def uninstall(package_name):
    for device in get_device_list():
        threading.Thread(target=uninstall_all, args=(device, package_name)).start()


def crash():
    for device in get_device_list():
        threading.Thread(target=export_crash, args=(device,)).start()
