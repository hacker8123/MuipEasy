# Writen by Hacker8123

import os
import re
import random
import string
import json
import requests
import urllib.parse
import hashlib
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
from tkinter import messagebox as tkmsgbox

# -------------------Modify Here According to Your Settings-------------------

_region = "dev_docker"
_host = "http://127.0.0.1:21051"
_sign = "9H2UrJ5J4yZJf95FqMkqi628snEmzvyV9oAp"
_ticket_len = 32
_cmd_id = 1116  # gmTalk

# ----------------------------------------------------------------------------

global_version = '0.1.2'
global_ui_sent = None
global_ui_resp = None
global_ui_uid = None
global_ui_weather = None
global_exec_history_count = 0
global_data_folder = './data/'


def sha256_sign(secret, message):
    sha256 = hashlib.sha256()
    sha256.update(f"{message}{secret}".encode())
    return sha256.hexdigest()


def execute(msg, add_history=False):
    if global_ui_uid.get()=='':
        tkmsgbox.showwarning(
                'Warning', 'Please input your uid.')
        return False
    try:
        kvs = []
        kvs.append(
            f"ticket={''.join(random.choice(string.ascii_letters) for i in range(_ticket_len))}")
        kvs.append(f"region={_region}")
        kvs.append(f"cmd={_cmd_id}")
        kvs.append(f"uid={global_ui_uid.get()}")
        kvs.append(f"msg={msg}")
        kvs.sort()

        qstr = f"{'&'.join(kvs)}"
        sign = sha256_sign(_sign, qstr)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=} while preparing query string")

    if add_history:
        global global_exec_history_count
        global_ui_sent.insert('1.0', f"{global_exec_history_count}: {msg}\n")
        global_exec_history_count += 1

    try:
        res = requests.get(
            f"{_host}/api?{urllib.parse.quote_plus(qstr, safe='=&')}&sign={sign}").content
        global_ui_resp.delete('1.0', tk.END)
        global_ui_resp.insert('1.0', res.decode())
        if res.decode().find('recv from nodeserver timeout') > 0:
            tkmsgbox.showwarning(
                'Timeout', 'Timeout. Maybe your uid is incorrect.')
            return False
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=} while forwarding request")

    return True


def read_number_from_file(filename):
    try:
        f = open(f'{global_data_folder}{filename}', encoding='utf-8')
        one_line = True
        result_list = []
        while one_line:
            one_line = f.readline()
            numbers = re.findall('\d+', one_line)
            if len(numbers) != 0:
                result_list += [numbers[0]]
        return result_list
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=} while reading file {filename}")


def func_infinite():
    if not execute('test if uid correct'):
        return
    execute('stamina infinite on')
    execute('energy infinite on')
    execute('wudi global avatar on')


def func_unlock_map():
    if not execute('test if uid correct'):
        return

    # first statue 第一座七天神像
    execute('quest accept 35205')
    execute('quest finish 35205')

    # statues 七天神像
    execute('openstate all 1')
    for statue_id in range(2, 29):
        execute('quest finish 303%02d' % statue_id)

    # SceneTransPoint 传送锚点
    trans_list = [10, 100, 103, 104, 105, 11, 114, 116, 12, 121, 122, 127, 128, 13, 14, 15, 152, 153, 154, 155, 156, 162, 165, 166, 167, 168, 180, 181, 182, 197, 200, 204, 205, 206, 208, 209, 210, 211, 212, 213, 214, 222, 225, 228, 234, 235, 236, 241, 242, 244, 245, 246, 247, 248, 249, 25, 250, 251, 252, 253, 254, 255, 256, 257, 258, 29, 293, 296, 298, 3, 301, 302, 304, 305, 306, 307, 316, 318, 319, 320, 321, 322, 324, 325, 326, 327, 328, 329, 33, 330, 331, 332, 34, 35, 356, 36, 365, 366, 37, 380, 381, 382, 383, 384, 4, 432, 435, 438, 442, 443, 444,
                  445, 446, 462, 463, 464, 465, 471, 472, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 5, 500, 501, 502, 517, 518, 519, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 555, 557, 558, 57, 575, 577, 58, 586, 587, 588, 589, 59, 598, 599, 6, 60, 602, 603, 604, 605, 606, 61, 612, 615, 616, 623, 625, 626, 652, 653, 655, 665, 670, 676, 69, 691, 7, 702, 703, 706, 72, 73, 74, 75, 76, 77, 78, 79, 8, 81, 82, 84, 85, 86, 87, 91, 92, 93, 95, 96, 97, 99]
    for trans_id in trans_list:
        execute('point 3 %d' % trans_id)

    # DungeonEntry 秘境入口
    dungeon_list = [1, 107, 117, 131, 133, 135, 137, 139, 146, 20, 22, 221, 282, 308, 310, 350, 351, 359,
                    361, 368, 40, 42, 424, 426, 433, 44, 45, 48, 50, 505, 507, 509, 516, 600, 607, 618, 646, 671, 674, 675]
    for dungeon_id in dungeon_list:
        execute('point 3 %d' % dungeon_id)

    # DungeonEntry(not 'SimpleUnlock'ed) 条件解锁的秘境
    dungeon2_list = [38, 218, 271, 396, 503, 731]  # 风龙、公子、龙王、女士、雷神、散兵
    for dungeon2_id in dungeon2_list:
        execute('point 3 %d' % dungeon2_id)

    # VirtualTransPoint 其它传送点
    virtual_list = [439, 468]  # 死兆星、群玉阁、566,570,580（幻影心流附近、甘金岛音乐、鹰翔海滩事件）
    for virtual_id in virtual_list:
        execute('point 3 %d' % virtual_id)

    # SceneVehicleSummonPoint 浪船锚点
    vehicle_list = [317, 323, 336, 337, 338, 339, 353, 363, 364, 378, 379, 385,
                    386, 387, 392, 393, 405, 458, 459, 475, 476, 477, 478, 514, 515, 571]
    for vehicle_id in vehicle_list:
        execute('point 3 %d' % vehicle_id)

    # test_list = []
    # PersonalSceneJumpPoint 未知
    # test_list=[177,178,179,190,27,28,287,288,30,31,32,345,402,416,579,581,583,585,611,88]
    # SceneBuildingPoint 地图上一些奇怪的符号比如海灯节
    # test_list=[151,157,158,159,160,161,170,201,207,215,216,226,227,231,238,259,268,273,286,341,342,343,344,354,370,371,372,373,374,375,388,391,400,401,408,409,410,411,412,413,414,415,423,428,429,434,467,511,523,524,525,526,527,528,529,530,531,532,54,55,56,563,564,565,574,578,62,622,624,63,64,65,650,669,686,687,688,694,695,696,726,98]
    # for test_id in test_list:
    #     execute('point 3 %d' % test_id)

def func_unlock_map2():
    if not execute('test if uid correct'):
        return

    execute('player level 60')

    # DungeonEntry(player level needed) 秘境入口(重新解锁，因为等级不够)
    dungeon_list = [1, 107, 117, 131, 133, 135, 137, 139, 146, 20, 22, 221, 282, 308, 310, 350, 351, 359,
                    361, 368, 40, 42, 424, 426, 433, 44, 45, 48, 50, 505, 507, 509, 516, 600, 607, 618, 646, 671, 674, 675]
    for dungeon_id in dungeon_list:
        execute('point 3 %d' % dungeon_id)


def func_graduate():
    if not execute('test if uid correct'):
        return
    execute('break 6')
    execute('level 90')
    execute('talent unlock all')
    execute('skill all 10')
    execute('item add 105 100000')


def func_get_all_avatar():
    if not execute('test if uid correct'):
        return
    for avatar_id in range(2, 100):
        execute('avatar add 100000%02d' % avatar_id)
    for costume_id in range(0, 6):
        execute('item add 3400%02d' % costume_id)


def func_get_all_weapon():
    if not execute('test if uid correct'):
        return
    weapon_list = read_number_from_file('weapon.txt')
    for weapon_id in weapon_list:
        execute('equip add %s 90 6 4' % weapon_id)
        execute('equip add %s 90 6 4' % weapon_id)


def func_get_all_item():
    if not execute('test if uid correct'):
        return

    # food 食物(2000)
    food_list = read_number_from_file('food.txt')
    for food_id in food_list:
        execute('item add %s 1000' % food_id)

    # recipe 食谱(1)
    recipe_list = read_number_from_file('recipe.txt')
    for recipe_id in recipe_list:
        execute('item add %s' % recipe_id)

    # gadget 小道具(1)
    gadget_exclude_list = {41, 50, 54, 55, 68, 69}
    for gadget_id in set(range(1, 76))-set(gadget_exclude_list):
        execute('item add 2200%02d' % gadget_id)

    # gadget consumeble 小道具消耗品(100)
    execute('item add 220017 50')  # 放热瓶
    execute('item add 220043 50')  # 四方八方之网
    execute('item add 220001 50')  # 共鸣石风
    execute('item add 220002 50')  # 共鸣石岩
    execute('item add 220032 50')  # 共鸣石雷
    execute('item add 220057 50')  # 共鸣石草

    # fireworks 烟花(1)
    for temp_id in set(range(1, 13)):
        execute('item add 2230%02d' % temp_id)

    # teapot realm unlock tool 洞天解锁道具(1)
    execute('item add 222001')  # 绘绮之枕印
    execute('item add 222002')  # 烟林之真果

    # money 钱币(42亿)
    execute('mcoin 10000000')  # 创世结晶
    execute('hcoin 10000000')  # 原石
    execute('scoin 10000000')  # 摩拉
    execute('home_coin 100000000')  # 家园币

    # gacha related 抽卡相关 (1000000)
    execute('item add 223 100000')  # 创世结晶
    execute('item add 224 100000')  # 相遇之缘
    execute('item add 221 100000')  # 星辉
    execute('item add 222 100000')  # 星尘

    # TODO: add more


def func_change_weather(event):
    if not execute('test if uid correct'):
        return
    execute(f'weather {global_ui_weather.get()}')


if __name__ == '__main__':

    ui_width = 360
    ui_height = 800
    ui_win = tk.Tk()
    ui_win.title(f'MuipEasy {global_version}')
    ui_win.geometry(f'{ui_width}x{ui_height}')

    ui_frm_uid = tk.Frame(master=ui_win)
    ui_lbl_uid = tk.Label(ui_frm_uid, text='uid', font=(None, 12))
    ui_lbl_uid.pack(side=tk.LEFT)
    ui_ent_uid = tk.Entry(ui_frm_uid, font=(None, 12), width=ui_width-40)
    ui_ent_uid.pack(side=tk.RIGHT)
    global_ui_uid = ui_ent_uid
    ui_frm_uid.pack(fill='x')

    ui_frm_msg = tk.Frame(master=ui_win)
    ui_lbl_msg = tk.Label(ui_frm_msg, text='msg', font=(None, 12))
    ui_lbl_msg.pack(side=tk.LEFT)
    ui_ent_msg = tk.Entry(ui_frm_msg, font=(None, 12), width=ui_width-40)
    ui_ent_msg.pack(side=tk.RIGHT)
    ui_frm_msg.pack(fill='x')

    ui_btn_execute = tk.Button(ui_win, text='Execute', font=(
        None, 12), command=lambda: execute(ui_ent_msg.get(), True))
    ui_btn_execute.pack()

    ui_lbl_sent = tk.Label(ui_win, text='Command History', font=(None, 12))
    ui_lbl_sent.pack()
    ui_txt_sent = tkscrolled.ScrolledText(
        master=ui_win, height=5, font=(None, 10))
    ui_txt_sent.pack()
    global_ui_sent = ui_txt_sent

    ui_lbl_resp = tk.Label(ui_win, text='Server Response', font=(None, 12))
    ui_lbl_resp.pack()
    ui_txt_resp = tkscrolled.ScrolledText(
        master=ui_win, height=4, font=(None, 10))
    ui_txt_resp.pack()
    global_ui_resp = ui_txt_resp

    ui_frm_init = tk.LabelFrame(
        ui_win, text="init unlock (must follow the order)", labelanchor="n", bg='#66CDAA')
    ui_lbl_init1 = tk.Message(ui_frm_init, text='1. After inital animation, follow Paimon and unlock first Teleport Waypoint.', font=(
        None, 12), anchor='w', width=ui_width-10, bg='#66CDAA')
    ui_lbl_init1.pack(fill='x')
    ui_btn_unlock_map = tk.Button(
        ui_frm_init, text='2. unlock map', font=(None, 12), command=func_unlock_map)
    ui_btn_unlock_map.pack(anchor='w')
    ui_lbl_init2 = tk.Message(ui_frm_init, text='3. Finish beating Slim quest.', font=(
        None, 12), anchor='w', width=ui_width-10, bg='#66CDAA')
    ui_lbl_init2.pack(fill='x')
    ui_btn_init_level60 = tk.Button(ui_frm_init, text='4.(optional) level 60, unlock more dungeon', font=(
        None, 12), command=func_unlock_map2)
    ui_btn_init_level60.pack(anchor='w')
    ui_btn_init_fly = tk.Button(ui_frm_init, text='5. accept fly quest', font=(
        None, 12), command=lambda: execute('quest accept 35603'))
    ui_btn_init_fly.pack(anchor='w')
    ui_lbl_init3 = tk.Message(ui_frm_init, text='6. Trans to Mondstadt, talk with Amber and fly to fountain. Then you will meet Dvalin, when start actual fight, use following button to finish.', font=(
        None, 12), anchor='w', width=ui_width-10, bg='#66CDAA')
    ui_lbl_init3.pack(fill='x')
    ui_btn_init_beat_dvalin = tk.Button(ui_frm_init, text='7. finish beat_dvalin quest', font=(
        None, 12), command=lambda: execute('quest finish 35722'))
    ui_btn_init_beat_dvalin.pack(anchor='w')
    ui_btn_init_restore_weather = tk.Button(ui_frm_init, text='8. accept restore_weather quest', font=(
        None, 12), command=lambda: execute('quest accept 30904'))
    ui_btn_init_restore_weather.pack(anchor='w')
    ui_frm_init.pack(fill=tk.X)

    ui_frm_init_extra = tk.LabelFrame(
        ui_win, text="init get items", labelanchor="n", bg='#66CDAA')
    ui_btn_graduate = tk.Button(ui_frm_init_extra, text='current avatar graduates', font=(
        None, 12), command=func_graduate)
    ui_btn_graduate.pack(anchor='w')
    ui_btn_get_all_avatar = tk.Button(ui_frm_init_extra, text='get all avatars', font=(
        None, 12), command=func_get_all_avatar)
    ui_btn_get_all_avatar.pack(anchor='w')
    ui_btn_get_all_weapon = tk.Button(ui_frm_init_extra, text='get all weapons', font=(
        None, 12), command=func_get_all_weapon)
    ui_btn_get_all_weapon.pack(anchor='w')
    ui_btn_get_all_item = tk.Button(ui_frm_init_extra, text='get all items (unfinished)', font=(
        None, 12), command=func_get_all_item)
    ui_btn_get_all_item.pack(anchor='w')
    ui_frm_init_extra.pack(fill=tk.X)

    ui_frm_daily = tk.LabelFrame(
        ui_win, text="daily", labelanchor="n", bg='#66CDAA')
    ui_btn_infinite = tk.Button(
        ui_frm_daily, text='infinite hp,stamina,energy', font=(None, 12), command=func_infinite)
    ui_btn_infinite.pack(anchor='w')
    ui_btn_kill_monster = tk.Button(ui_frm_daily, text='kill all monsters', font=(
        None, 12), command=lambda: execute('kill monster all'))
    ui_btn_kill_monster.pack(anchor='w')
    ui_frm_weather = tk.Frame(master=ui_frm_daily)
    ui_lbl_weather = tk.Label(ui_frm_weather, text='weather', font=(None, 12))
    ui_lbl_weather.pack(side=tk.LEFT)
    ui_box_weather = ttk.Combobox(ui_frm_weather)
    ui_box_weather['value'] = ('sun', 'hot', 'heat', 'cloud', 'rain', 'thuner', 'storm',
                               'lightning', 'snow', 'freeze', 'frost', 'ice', 'mist', 'fog', 'desert')
    ui_box_weather.current(0)
    ui_box_weather.bind("<<ComboboxSelected>>", func_change_weather)
    global_ui_weather = ui_box_weather
    ui_box_weather.pack()
    ui_frm_weather.pack(anchor='w')
    ui_frm_daily.pack(fill=tk.X)

    ui_win.mainloop()
