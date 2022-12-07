import json
import sys
import random
import os
from os import system, chdir, getcwd
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtUiTools import loadUiType
form_class = loadUiType("washer.ui")[0]
var_path_from_getcwd = getcwd()

class WindowClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pushButton_Apl.clicked.connect(self.generateApl)
        self.pushButton_Run.clicked.connect(self.runDmake)

    def LoadFromJson(self, json_file_name):
        with open(json_file_name, 'rb') as f:
            return json.load(f)

    def GEA_json2lua(self, data, retract=1):
        temp_str = ""
        num_keys = len(data.keys())

        for i, key in enumerate(data.keys()):
            temp_str += "    wash_step.sub_cycle_update({{ sub_cycle = \'{}\' }}),\n".format(key)
            temp_str += "    wash_step.pause({{ seconds = {} }})".format(data[key])
            if i < num_keys-1:
                temp_str += ",\n"

        return temp_str

    def SaveToLua(self, data, lua_file_name, note=''):
        lua_str = "--[[\n{}\n]]\n\nreturn ".format(note)
        lua_str += "wash_step.sequence("
        lua_str += "{\n"
        with open(lua_file_name, 'wb') as f:
            lua_str += "  steps = {\n"
            lua_str += self.GEA_json2lua(data)
            lua_str += "\n"
            lua_str += "  }\n"
            lua_str += "})"
            f.write(lua_str.encode("utf-8"))

    def generateApl(self) :
        # raw data -> json
        chdir(var_path_from_getcwd)
        print(var_path_from_getcwd)

        print(self.lineEdit_Fill.text())
        dic ={ "fill" : self.lineEdit_Fill.text(),
               "wash" : self.lineEdit_Wash.text(),
               "spin" : self.lineEdit_Spin.text(),
               "drain" : self.lineEdit_Drain.text() }
        print(json.dumps(dic, indent=4))

        with open('washerUi.json', 'w') as f :
            json.dump(dic, f, indent=4)

        # json -> lua
        loadedJson = self.LoadFromJson('washerUi.json')
        gpath = "/Users/jessie/GEA_Code/laundry.washer-global-front-load-2019-source-snapshot/Parametric/lua/data/global_front_load/model_data/cycles"
        chdir(gpath)
        print(gpath)

        self.SaveToLua(loadedJson, "diy_cycle.lua", "Diy Cycle")

    def runDmake(self) :
        dpath = "/Users/jessie/GEA_Code/laundry.washer-global-front-load-2019-source-snapshot"
        chdir(dpath)
        print(dpath)

        system("dmake -f gfl-mc-target.mk package -j16 RELEASE=N DEBUG=N")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()