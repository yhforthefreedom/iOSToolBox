# coding:utf-8
import json
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import time
from tkinter import filedialog
import subprocess
from collections import Counter
import shutil


# tkinter制作界面
class APKTk:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('800x200')
        self.root.title("ios工具箱    作者:Tsissan    QQ:834528842")
        self.path = StringVar()
        self.path.set("请输入需要安装的apk完整路径")
        self.package_name = StringVar()
        self.package_name.set("请选择app的包名")
        self.select_device_list = []
        self.device_list = self.get_device_list()
        self.cb_list = []
        self.package_3 = self.show_package()
        self.perf_index = StringVar()
        self.perf_index.set('请选择需要关注的性能指标,不选择代表关注全部指标')

    @staticmethod
    def install_and_open(device_name, file_path):
        # 安装app
        subprocess.call("tidevice --udid " + device_name + " install " + file_path)

    @staticmethod
    def package_info(device_name):
        # 获取设备的具体信息
        subprocess.call(f"tidevice --udid {device_name} info")

    def collect_pref(self, device_name, package_name):
        # 采集性能
        perf_index = self.perf_index.get()
        if perf_index == '请选择需要关注的性能指标,不选择代表关注全部指标':
            subprocess.call(f"tidevice --udid {device_name} perf -B {package_name}")
        else:
            subprocess.call(f"tidevice --udid {device_name} perf -o {perf_index} -B {package_name}")

    @staticmethod
    def close_pref(device_name):
        # 关闭采集
        res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for i in str(res).split(r'\n'):
            if device_name in i:
                pid = re.findall(r'(\d+)', i)[-1]
                subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
                print('采集性能服务停止！')

    def choose_perf(self):
        values = ['cpu', 'memory', 'fps', 'gpu', 'network']
        comboxlist_perf = ttk.Combobox(self.root, textvariable=self.perf_index, state='readonly', values=values,
                                       width=62)
        self.cb_list.append(comboxlist_perf)
        comboxlist_perf.grid(row=len(self.device_list) + 3, column=0)

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
        if not os.path.exists("D:/ios_screenshot"):
            os.mkdir("D:/ios_screenshot")
        image = f'{str(time.strftime("%Y%m%d%H%M%S", time.localtime()))}_{device_name}.png'
        subprocess.call(f"tidevice --udid {device_name} screenshot D:/ios_screenshot/{image}")
        print(f"设备{device_name}的截图保存在D:/ios_screenshot目录的{image}")

    @staticmethod
    def check_process(device_name, package_name):
        # 查看进程
        if package_name == '' or package_name == '请选择app的包名':
            subprocess.call(f'tidevice --udid {device_name} ps')
        else:
            print(f"设备{device_name}的应用{package_name}当前进程信息：")
            subprocess.call(f"tidevice --udid {device_name} ps | findstr {package_name}", shell=True)

    @staticmethod
    def output_log(device_name):
        # 导出缓存日志
        if not os.path.exists("D:/ios_log"):
            os.mkdir("D:/ios_log")
        log_name = f'{str(time.strftime("%Y%m%d%H%M%S", time.localtime()))}_{device_name}.txt'
        subprocess.call(f"tidevice --udid {device_name} syslog > D:/ios_log/{log_name}", shell=True)
        print(f"设备{device_name}的日志保存在D:/ios_log目录的{log_name}")

    @staticmethod
    def close_output_log(device_name):
        # 关闭日志输出
        res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for i in str(res).split(r'\n'):
            if device_name in i:
                pid = re.findall(r'(\d+)', i)[-1]
                subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
                print('日志导出服务停止！,请在D:/ios_log查看')

    @staticmethod
    def uninstall_all(device_name, package_name):
        # 卸载app
        subprocess.call("tidevice --udid " + device_name + " uninstall " + package_name)

    @staticmethod
    def get_device_list():
        res = subprocess.check_output("tidevice list")
        try:
            device_list = [i.split()[0] for i in res.decode('gbk').strip().split('\n')[1:]]
            return device_list
        except IndexError:
            return []

    def mul_check_box(self):
        try:
            for index, item in enumerate(self.device_list):
                ios_mes = subprocess.check_output("tidevice --udid " + item + ' info | findstr '
                                                                              '"MarketName ProductVersion"',
                                                  shell=True).decode('gbk') \
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
        self.package_3 = self.show_package()
        self.combobox_list()
        self.choose_perf()
        self.input_text()
        self.path_button()
        self.install_button()
        self.launch_button()
        self.refresh_button()
        self.activity_button()
        self.screenshot_button()
        self.clear_button()
        self.kill_button()
        self.check_button()
        self.export_button()
        self.monkey_button()
        self.uninstall_button()
        self.close_pref_button()
        self.close_output_button()
        self.export_crash_button()

    def show_package(self):
        packages = []
        for i in self.device_list:
            res = subprocess.check_output(f"tidevice --udid {i} applist")
            packages_list = res.decode('gbk').split('\n')[:-1]
            for j in packages_list:
                packages.append(j)
        c = dict(Counter(packages))
        return [i for i in c.keys() if c[i] == len(self.device_list)]

    @staticmethod
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

    def combobox_list(self):
        comboxlist = ttk.Combobox(self.root, textvariable=self.package_name, state='readonly', values=self.package_3,
                                  width=62)
        self.cb_list.append(comboxlist)
        comboxlist.grid(row=len(self.device_list) + 1, column=0)

    def path_button(self):
        button_path = Button(self.root, text="选择文件", command=self.select_path)
        button_path.grid(row=len(self.device_list), column=1)
        self.cb_list.append(button_path)

    def install_button(self):
        button_install = Button(self.root, text="安装APP", command=self.install)
        button_install.grid(row=len(self.device_list), column=2)
        self.cb_list.append(button_install)

    def refresh_button(self):
        button_refresh = Button(self.root, text="刷新设备", command=self.refresh_data)
        button_refresh.grid(row=len(self.device_list), column=3)
        self.cb_list.append(button_refresh)

    def activity_button(self):
        button_activity = Button(self.root, text="应用列表", command=self.activity)
        button_activity.grid(row=len(self.device_list) + 1, column=1)
        self.cb_list.append(button_activity)

    def launch_button(self):
        button_launch = Button(self.root, text="启动应用", command=self.launch)
        button_launch.grid(row=len(self.device_list) + 1, column=2)
        self.cb_list.append(button_launch)

    def screenshot_button(self):
        button_screenshot = Button(self.root, text="手机截图", command=self.screen)
        button_screenshot.grid(row=len(self.device_list), column=5)
        self.cb_list.append(button_screenshot)

    def clear_button(self):
        button_clear = Button(self.root, text="采集性能", command=self.perf)
        button_clear.grid(row=len(self.device_list) + 3, column=1)
        self.cb_list.append(button_clear)

    def close_pref_button(self):
        button_clear = Button(self.root, text="关闭采集", command=self.off_perf)
        button_clear.grid(row=len(self.device_list) + 3, column=2)
        self.cb_list.append(button_clear)

    def kill_button(self):
        button_kill = Button(self.root, text="杀掉应用", command=self.kill)
        button_kill.grid(row=len(self.device_list) + 1, column=3)
        self.cb_list.append(button_kill)

    def check_button(self):
        button_check = Button(self.root, text="查看进程", command=self.check)
        button_check.grid(row=len(self.device_list) + 1, column=4)
        self.cb_list.append(button_check)

    def export_button(self):
        button_export = Button(self.root, text="导出日志", command=self.export)
        button_export.grid(row=len(self.device_list) + 3, column=3)
        self.cb_list.append(button_export)

    def close_output_button(self):
        button_export = Button(self.root, text="关闭导出", command=self.off_output)
        button_export.grid(row=len(self.device_list) + 3, column=4)
        self.cb_list.append(button_export)

    def monkey_button(self):
        button_monkey = Button(self.root, text="设备信息", command=self.run)
        button_monkey.grid(row=len(self.device_list), column=4)
        self.cb_list.append(button_monkey)

    def uninstall_button(self):
        button_uninstall = Button(self.root, text="一键卸载", command=self.uninstall)
        button_uninstall.grid(row=len(self.device_list) + 1, column=5)
        self.cb_list.append(button_uninstall)

    def input_text(self):
        entry_log = Entry(self.root, width=65, textvariable=self.path)
        entry_log.grid(row=len(self.device_list), column=0, sticky='w')
        self.cb_list.append(entry_log)

    def export_crash_button(self):
        crash_button = Button(self.root, text="崩溃日志", command=self.crash)
        crash_button.grid(row=len(self.device_list) + 3, column=5)
        self.cb_list.append(crash_button)

    def get_apk_name(self):
        return self.path.get()

    def get_package_name(self):
        return self.package_name.get().split()[0]

    def devices_list(self):
        selected_device_list = [i.get() for i in self.select_device_list if i.get()]
        print(selected_device_list)
        return selected_device_list

    def mainloop(self):
        self.root.mainloop()

    def install(self):
        apk_name = self.get_apk_name()
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

    def crash(self):
        for device in self.devices_list():
            threading.Thread(target=self.export_crash, args=(device,)).start()


if __name__ == '__main__':
    apkTk = APKTk()
    apkTk.mul_check_box()
    apkTk.choose_perf()
    apkTk.combobox_list()
    apkTk.input_text()
    apkTk.path_button()
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
    apkTk.export_crash_button()
    apkTk.root.mainloop()
