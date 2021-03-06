from PyQt5 import QtWidgets, QtCore, QtGui
from JPEGUtils.utils import read_all_jpegs_in_dir, read_all_metadata_tags_in_files, files_containing_tags
import os
from UI.config import *
import shutil
import random
import sys

class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.base_dir = None
        self.meta_tags = tuple()
        self.update_directory()
        if self.base_dir is None:
            self.close()
        else:
            # Show a dialog box
            self.setWindowTitle(WINDOW_TITLE)
            self.setGeometry(100, 100, 10, 10)  # Minimal size
            # Setu the Icon
            self.setWindowIcon(QtGui.QIcon(LOGO_PATH))

            central_widget = QtWidgets.QWidget(self)
            self.setCentralWidget(central_widget)
            self.layout = QtWidgets.QGridLayout()
            central_widget.setLayout(self.layout)
            # Create an internal layout for the checkboxes
            self.search_button_any = QtWidgets.QPushButton(SEARCH_BUTTON_TEXT_ANY)
            self.search_button_any.clicked.connect(lambda: self.search_button_clicked(mode="any"))
            self.search_button_all = QtWidgets.QPushButton(SEARCH_BUTTON_TEXT_ALL)
            self.search_button_all.clicked.connect(lambda: self.search_button_clicked(mode="all"))
            # Show a label at the top of the window in bold
            self.label = QtWidgets.QLabel(FILTER_BY_TAGS_BUTTON_TEXT)
            self.label.setFont(QtGui.QFont("Arial", weight=QtGui.QFont.Bold))
            self.label.setAlignment(QtCore.Qt.AlignLeft)
            self.layout.addWidget(self.label, 0, 0)
            self.checkboxes = {}
            if self.base_dir is not None:
                self.show_filter_dialog(images_dir=self.base_dir)
            self.show()

    def update_directory(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, SELECT_FOLDER)
        # Check that the directory exists
        if os.path.exists(directory):
            self.base_dir = directory
            img_paths = read_all_jpegs_in_dir(dir_path=directory, recursive=True)
            self.meta_tags = read_all_metadata_tags_in_files(img_paths=img_paths)
        else:
            self.base_dir = None
            self.show_error(INVALID_DIR)

    def show_error(self, error: str) -> None:
        QtWidgets.QMessageBox.about(self, "Error", error)

    def show_filter_dialog(self, images_dir) -> None:
        img_paths = tuple()
        if images_dir is not None:
            img_paths = read_all_jpegs_in_dir(dir_path=images_dir, recursive=True)
        if len(img_paths) > 0:
            self.meta_tags = read_all_metadata_tags_in_files(img_paths=img_paths)
            unique_tags = set()
            for img_path, img_tags in self.meta_tags:
                if img_tags is not None:
                    unique_tags.update(img_tags)
            self.delete_checkboxes()
            self.checkboxes = {tag: QtWidgets.QCheckBox(tag) for tag in sorted(tuple(unique_tags))}
            self.show_checkboxes()
        else:
            self.show_error(NO_IMAGES_IN_DIR)
            # Close the window
            self.close()
            self.cleanup()
            sys.exit(0)

    def show_checkboxes(self, grid_shape=3) -> None:
        for i, checkbox in enumerate(self.checkboxes.values()):
            self.layout.addWidget(checkbox, i // grid_shape + 1, i % grid_shape)

        # Add the search buttons
        self.layout.addWidget(self.search_button_any, len(self.checkboxes)//grid_shape + 2, 0, 1, grid_shape)
        self.layout.addWidget(self.search_button_all, len(self.checkboxes)//grid_shape + 3, 0, 1, grid_shape)

    def delete_checkboxes(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setParent(None)
        # Delete the search button
        self.search_button_any.setParent(None)
        self.search_button_all.setParent(None)
        self.checkboxes = {}

    def search_button_clicked(self, mode="any") -> None:
        # Build a tmp directory in from the working directory
        tmp_dir = os.path.join(os.getcwd(), TMP_DIR)
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        else:
            shutil.rmtree(tmp_dir)
            os.mkdir(tmp_dir)
        # Get the images that match the tags
        # Get the checked checkboxes
        checked_tags = tuple(str(key) for key, checkbox in self.checkboxes.items() if checkbox.isChecked())
        img_paths = files_containing_tags(self.meta_tags, tags=checked_tags, mode=mode)
        # Create a copy to the img_paths in the tmp directory
        for img in img_paths:
            img_path = os.path.join(tmp_dir, os.path.basename(img))
            if os.path.exists(img_path):
                # Append a random number to the file name
                file_name, file_extension = os.path.splitext(img_path)
                img_path = file_name + str(random.randint(0, 10000)) + file_extension
            # Make a copy, making sure that it will have permissions to be deleted later
            shutil.copy(img, img_path)
            os.chmod(img_path, 0o777)

        # Open the tmp directory in the default file manager
        os.system("start " + tmp_dir)

    def cleanup(self) -> None:
        self.delete_checkboxes()
        self.base_dir = None
        self.meta_tags = tuple()
        # Delete the tmp directory
        tmp_dir = os.path.join(os.getcwd(), TMP_DIR)
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    def __del__(self):
        self.cleanup()

    def __exit__(self):
        self.cleanup()