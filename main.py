from PyQt5 import QtWidgets
import sys
from UI.GUI import GUI
import os
from UI.config import TMP_DIR
import shutil

# Execute this function before dying
def cleanup():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    exec_result = app.exec_()
    cleanup()
    sys.exit(exec_result)