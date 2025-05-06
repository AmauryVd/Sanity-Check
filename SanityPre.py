from PySide2 import QtWidgets, QtCore
import sys
from enum import Enum, auto

import maya.cmds as cmds

# Vérifications avec leurs solutions
library_to_check = {
    "Nom de l'objet": {
        "check": lambda: "pCube1" in cmds.ls(),
        "fix": lambda: cmds.polyCube(name="pCube1") if not cmds.ls("pCube1") else None
    },
    "Check transformation": {
        "check": lambda: cmds.getAttr("pCube1.translateX") == 1 if cmds.ls("pCube1") else False,
        "fix": lambda: cmds.setAttr("pCube1.translateX", 1) if cmds.ls("pCube1") else None
    },
    "Avoir un matériau appliqué": {
        "check": lambda: cmds.ls(materials=True),
        "fix": lambda: cmds.shadingNode("lambert", asShader=True) if not cmds.ls(materials=True) else None
    },
}


class SanityStatus(Enum):
    FAIL = auto()
    OK = auto()



san_result = SanityStatus.FAIL
excepted_result = SanityStatus.OK



class ChecklistApp(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ChecklistApp, self).__init__(parent)
        self.setWindowTitle("Sanity Check")
        self.resize(400, 400)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.checklist = QtWidgets.QListWidget()
        for item in library_to_check.keys():
            list_item = QtWidgets.QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            list_item.setCheckState(QtCore.Qt.Unchecked)
            self.checklist.addItem(list_item)
        self.layout.addWidget(self.checklist)

        self.result_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.result_list)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.check_button = QtWidgets.QPushButton("Run")
        self.check_button.clicked.connect(self.run_checks)
        self.button_layout.addWidget(self.check_button)

        self.fix_button = QtWidgets.QPushButton("Fix")
        self.fix_button.clicked.connect(self.fix_issues)
        self.button_layout.addWidget(self.fix_button)

        self.layout.addLayout(self.button_layout)

        self.additional_button_layout = QtWidgets.QHBoxLayout()
        self.tick_all_button = QtWidgets.QPushButton("Tick All")
        self.tick_all_button.clicked.connect(self.tick_all_tasks)
        self.additional_button_layout.addWidget(self.tick_all_button)

        self.untick_all_button = QtWidgets.QPushButton("Untick All")
        self.untick_all_button.clicked.connect(self.untick_all_tasks)
        self.additional_button_layout.addWidget(self.untick_all_button)

        self.run_all_button = QtWidgets.QPushButton("Run All")
        self.run_all_button.clicked.connect(self.run_all_tasks)
        self.additional_button_layout.addWidget(self.run_all_button)

        self.fix_all_button = QtWidgets.QPushButton("Fix All")
        self.fix_all_button.clicked.connect(self.fix_all_tasks)
        self.additional_button_layout.addWidget(self.fix_all_button)

        self.layout.addLayout(self.additional_button_layout)

    def update_task_label(self, list_item, state):
        """
        Met à jour le style visuel d'un élément de liste selon son état.
        """
        if state == "OK":
            list_item.setBackground(QtCore.Qt.green)
            list_item.setForeground(QtCore.Qt.darkGreen)
        elif state == "Fail":
            list_item.setBackground(QtCore.Qt.red)
            list_item.setForeground(QtCore.Qt.white)

    def run_checks(self):
        """
        Exécute les vérifications sélectionnées dans la checklist.
        """
        self.result_list.clear()

        for i in range(self.checklist.count()):
            item = self.checklist.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                check_name = item.text()
                result = library_to_check[check_name]["check"]()
                result_text = f"{check_name}: {'OK' if result else 'Fail'}"

                result_item = QtWidgets.QListWidgetItem(result_text)
                self.result_list.addItem(result_item)

                self.update_task_label(result_item, "OK" if result else "Fail")

    def run_all_tasks(self):
        """
        Exécute toutes les vérifications, cochées ou non.
        """
        self.result_list.clear()

        for i in range(self.checklist.count()):
            item = self.checklist.item(i)
            check_name = item.text()
            result = library_to_check[check_name]["check"]()
            result_text = f"{check_name}: {'OK' if result else 'Fail'}"

            result_item = QtWidgets.QListWidgetItem(result_text)
            self.result_list.addItem(result_item)

            self.update_task_label(result_item, "OK" if result else "Fail")

    def fix_issues(self):
        """
        Corrige les problèmes identifiés comme "Fail" parmi les tâches cochées.
        """
        for i in range(self.result_list.count()):
            result_item = self.result_list.item(i)
            result_text = result_item.text()
            check_name, status = result_text.split(": ")
            if status == "Fail":
                library_to_check[check_name]["fix"]()

        self.run_checks()

    def fix_all_tasks(self):
        """
        Corrige tous les problèmes, cochés ou non.
        """
        for check_name in library_to_check.keys():
            if not library_to_check[check_name]["check"]():
                library_to_check[check_name]["fix"]()

        self.run_all_tasks()

    def tick_all_tasks(self):
        """
        Coche toutes les tâches dans la checklist.
        """
        for i in range(self.checklist.count()):
            self.checklist.item(i).setCheckState(QtCore.Qt.Checked)

    def untick_all_tasks(self):
        """
        Décoche toutes les tâches dans la checklist.
        """
        for i in range(self.checklist.count()):
            self.checklist.item(i).setCheckState(QtCore.Qt.Unchecked)

def main():
    global app, maya_window
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    maya_window = ChecklistApp()
    maya_window.show()





if __name__ == "__main__":
    main()