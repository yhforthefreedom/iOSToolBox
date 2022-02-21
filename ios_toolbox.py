# coding:utf-8
import json
import os
import random
import tkinter as tk
from tkinter import *
import threading
import time
from tkinter import filedialog
import subprocess


# tkinter制作界面
class APKTk:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('800x200')
        self.root.title("ios工具箱    作者:Tsissan    QQ:834528842")
        self.path = StringVar()
        self.path.set("请输入需要安装的apk完整路径")
        self.package_name = StringVar()
        self.package_name.set("请输入app的包名")
        self.select_device_list = []
        self.device_list = self.get_device_list()
        self.cb_list = []

    @staticmethod
    def install_and_open(device_name, file_path):
        # 安装app
        subprocess.call("tidevice --udid " + device_name + " install " + file_path)

    @staticmethod
    def package_info(device_name):
        # 获取设备的具体信息
        subprocess.call(f"tidevice --udid {device_name} info")

    @staticmethod
    def collect_pref(device_name, package_name):
        # 采集性能
        try:
            subprocess.call(f"tidevice --udid {device_name} perf -B {package_name}")
        except KeyboardInterrupt:
            print("请重启ios工具箱")

    @staticmethod
    def close_pref(device_name):
        # 关闭采集
        res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for i in str(res).split(r'\n'):
            if device_name in i:
                pid = re.findall(r'(\d+)', i)[-1]
                subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
                print('采集性能服务停止！')

    @staticmethod
    def kill_process(device_name, package_name):
        # 强制杀死app
        subprocess.call(f"tidevice --udid {device_name} kill {package_name}")

    @staticmethod
    def get_activity(device_name):
        # 获取设备已安装应用
        print(f"设备{device_name}已安装应用：")
        subprocess.call(f"tidevice --udid {device_name} applist")

    @staticmethod
    def launch_app(device_name, package_name):
        subprocess.call(f'tidevice --udid {device_name} launch {package_name}')

    @staticmethod
    def screenshot(device_name):
        # 手机截图
        if os.path.exists("D:/ios_screenshot"):
            pass
        else:
            os.mkdir("D:/ios_screenshot")
        image = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        random_str = str(random.randint(0, 100))
        subprocess.call(f"tidevice --udid {device_name} screenshot D:/ios_screenshot/{image}_{random_str}.png")
        print(f"设备{device_name}的截图已保存在D:/ios_screenshot目录下")

    @staticmethod
    def check_process(device_name, package_name):
        # 查看进程
        if package_name == '' or package_name == '请输入app的包名':
            subprocess.call(f'tidevice --udid {device_name} ps')
        else:
            print(f"设备{device_name}的应用{package_name}当前进程信息：")
            subprocess.call(f"tidevice --udid {device_name} ps | findstr {package_name}", shell=True)

    @staticmethod
    def output_log(device_name):
        # 导出缓存日志
        if os.path.exists("D:/ios_log"):
            pass
        else:
            os.mkdir("D:/ios_log")
        try:
            subprocess.call("tidevice --udid " + device_name + " syslog > D:/ios_log/" + str(
                time.strftime("%Y%m%d%H%M%S", time.localtime())) + "_" + str(random.randint(0, 100)) + ".txt",
                            shell=True)
        except KeyboardInterrupt:
            print("请重启ios工具箱")

    @staticmethod
    def close_output_log(device_name):
        # 关闭日志输出
        res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for i in str(res).split(r'\n'):
            if device_name in i:
                pid = re.findall(r'(\d+)', i)[-1]
                subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
                print('日志导出服务停止！,请在D:/android_log查看')

    @staticmethod
    def uninstall_all(device_name, package_name):
        # 卸载app
        subprocess.call("tidevice --udid " + device_name + " uninstall " + package_name)

    @staticmethod
    def get_device_list():
        res = subprocess.check_output("tidevice list")
        device_list = [i[0:24] for i in res.decode().split('\n') if len(i) > 25]
        return device_list

    def mul_check_box(self):
        try:
            print("制作多选框", self.device_list)
            for index, item in enumerate(self.device_list):
                ios_mes = subprocess.check_output("tidevice --udid " + item + ' info | findstr '
                                                                              '"MarketName ProductVersion"',
                                                  shell=True).decode() \
                    .strip('\n').split('\n')
                ios_market_name = ios_mes[0].split(':')[-1].strip()
                ios_version = ios_mes[-1].split(':')[-1].strip()

                device_mes = {
                    "手机型号": ios_market_name,
                    "iOS版本": ios_version
                }
                device_mes = json.dumps(device_mes, ensure_ascii=False)
                device_info = item + '\n' + device_mes
                self.select_device_list.append(tk.StringVar())
                cb = Checkbutton(self.root, text=device_info, variable=self.select_device_list[-1],
                                 onvalue=item, offvalue='')
                self.cb_list.append(cb)
                cb.grid(row=index, column=0, sticky='w')
                cb.select()
        except:
            pass

    def select_path(self):
        # 选择文件
        file_path = filedialog.askopenfilename()
        self.path.set(file_path)
        return file_path

    # 刷新设备列表
    def refresh_data(self):
        print("重新获取设备信息")
        for item in self.cb_list:
            item.destroy()
        self.cb_list = []
        self.device_list = self.get_device_list()
        self.select_device_list = []
        self.mul_check_box()

    def path_button(self):
        Button(self.root, text="选择文件", command=self.select_path).grid(row=len(self.device_list) + 2, column=1)

    def install_button(self):
        button_install = Button(self.root, text="安装APP", command=self.install)
        button_install.grid(row=len(self.device_list) + 2, column=2)

    def refresh_button(self):
        button_install = Button(self.root, text="刷新设备", command=self.refresh_data)
        button_install.grid(row=len(self.device_list) + 2, column=3)

    def activity_button(self):
        Button(self.root, text="应用列表", command=self.activity).grid(row=len(self.device_list) + 3, column=1)

    def launch_button(self):
        Button(self.root, text="启动应用", command=self.launch).grid(row=len(self.device_list) + 3, column=2)

    def screenshot_button(self):
        button_activity = Button(self.root, text="手机截图", command=self.screen)
        button_activity.grid(row=len(self.device_list) + 2, column=5)

    def clear_button(self):
        button_clear = Button(self.root, text="采集性能", command=self.perf)
        button_clear.grid(row=len(self.device_list) + 4, column=1)

    def close_pref_button(self):
        button_clear = Button(self.root, text="关闭采集", command=self.off_perf)
        button_clear.grid(row=len(self.device_list) + 4, column=2)

    def kill_button(self):
        button_kill = Button(self.root, text="杀掉应用", command=self.kill)
        button_kill.grid(row=len(self.device_list) + 3, column=3)

    def check_button(self):
        button_check = Button(self.root, text="查看进程", command=self.check)
        button_check.grid(row=len(self.device_list) + 3, column=4)

    def export_button(self):
        button_export = Button(self.root, text="导出日志", command=self.export)
        button_export.grid(row=len(self.device_list) + 4, column=3)

    def close_output_button(self):
        button_export = Button(self.root, text="关闭导出", command=self.off_output)
        button_export.grid(row=len(self.device_list) + 4, column=4)

    def monkey_button(self):
        button_install = Button(self.root, text="设备信息", command=self.run)
        button_install.grid(row=len(self.device_list) + 2, column=4)

    def uninstall_button(self):
        button_gdt = Button(self.root, text="一键卸载", command=self.uninstall)
        button_gdt.grid(row=len(self.device_list) + 3, column=5)

    def input_text(self):
        entry_log = Entry(self.root, width=65, textvariable=self.path)
        entry_log.grid(row=len(self.device_list) + 2, column=0, sticky='w')

    def input_package(self):
        package_log = Entry(self.root, width=65, textvariable=self.package_name)
        package_log.grid(row=len(self.device_list) + 3, column=0, sticky='w')

    def get_apk_name(self):
        return self.path.get()

    def get_package_name(self):
        return self.package_name.get()

    def devices_list(self):
        selected_device_list = [i.get() for i in self.select_device_list if i.get()]
        print(selected_device_list)
        return selected_device_list

    def mainloop(self):
        self.root.mainloop()

    def install(self):
        apk_name = self.get_apk_name()
        print(apk_name)
        for device in self.devices_list():
            threading.Thread(target=self.install_and_open, args=(device, apk_name)).start()

    def run(self):
        for device in self.devices_list():
            threading.Thread(target=self.package_info, args=(device,)).start()

    def launch(self):
        package_name = self.get_package_name()

        for device in self.devices_list():
            threading.Thread(target=self.launch_app, args=(device, package_name)).start()

    def perf(self):
        package_name = self.get_package_name()

        for device in self.devices_list():
            threading.Thread(target=self.collect_pref, args=(device, package_name)).start()

    def off_perf(self):
        for device in self.devices_list():
            threading.Thread(target=self.close_pref, args=(device,)).start()

    def kill(self):
        package_name = self.get_package_name()

        for device in self.devices_list():
            threading.Thread(target=self.kill_process, args=(device, package_name)).start()

    def activity(self):
        for device in self.devices_list():
            threading.Thread(target=self.get_activity, args=(device,)).start()

    def screen(self):
        for device in self.devices_list():
            threading.Thread(target=self.screenshot, args=(device,)).start()

    def check(self):
        package_name = self.get_package_name()

        for device in self.devices_list():
            threading.Thread(target=self.check_process, args=(device, package_name)).start()

    def export(self):
        for device in self.devices_list():
            threading.Thread(target=self.output_log, args=(device,)).start()

    def off_output(self):
        for device in self.devices_list():
            threading.Thread(target=self.close_output_log, args=(device,)).start()

    def uninstall(self):
        package_name = self.get_package_name()
        for device in self.devices_list():
            threading.Thread(target=self.uninstall_all, args=(device, package_name)).start()


if __name__ == '__main__':
    apkTk = APKTk()
    apkTk.mul_check_box()
    apkTk.input_text()
    apkTk.path_button()
    apkTk.input_package()
    apkTk.install_button()
    apkTk.launch_button()
    apkTk.refresh_button()
    apkTk.activity_button()
    apkTk.screenshot_button()
    apkTk.clear_button()
    apkTk.kill_button()
    apkTk.check_button()
    apkTk.export_button()
    apkTk.monkey_button()
    apkTk.uninstall_button()
    apkTk.close_pref_button()
    apkTk.close_output_button()
    apkTk.root.mainloop()
