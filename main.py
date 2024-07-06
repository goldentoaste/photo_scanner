from genericpath import isdir, isfile
import os
import subprocess
import sys
from time import sleep
from typing import List, Tuple

from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

from MainWindow import Ui_MainWindow


class ShellRunner(QThread):
    shellRes = pyqtSignal(object)  # emits (key, result) or (key, list of all result)
    SUCCESS = "success"
    ERROR = "error"

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        self.__queue: List[Tuple[str, str, bool]] = []

    def run(self) -> None:
        while True:
            if self.__queue:
                key, cmd, complete = self.__queue.pop(0)
                self.executeShell(key, cmd, complete)
            sleep(0.1)

    def queueCommand(self, key: str, cmd: str, complete: bool):
        self.__queue.append((key, cmd, complete))

    def executeShell(self, key: str, cmd: str, complete):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if p.stdout:
            if complete:
                out = []
                for line in p.stdout.readlines():
                    out.append(str(line, "utf8").strip())

                # return all results as one emit
                self.shellRes.emit((key, out))
            else:
                for line in p.stdout.readlines():
                    # a seperate emit for each emit.
                    self.shellRes.emit((key, line))

        self.shellRes.emit((key, self.SUCCESS if p.wait() == 0 else self.ERROR))


class PhotoScanner(QMainWindow, Ui_MainWindow):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.show()

    def initUi(self):

        # setup gui properties
        self.consoleLog.setMaximumBlockCount(200)
        self.consoleLog.setReadOnly(True)
        self.dpiSelect.setEditText("600")

        self.shellRunner = ShellRunner(self)
        self.lastDir = ""
        self.fileIndex = 1

        # setup gui events
        self.outpathButton.clicked.connect(self.getOutputPath)
        self.scanBtn.clicked.connect(self.scan)

        # setup gui values
        self.shellRunner.shellRes.connect(self.setupScanners)
        self.shellRunner.queueCommand("setupScanners", "naps2.console --listdevices --driver twain", True)
        self.log("Loading Scanner devices")

        self.dpiSelect.setCurrentText("600")

        self.shellRunner.start()

    def getOutputPath(self):
        path = QFileDialog.getExistingDirectory(self, "Select output directory", self.lastDir)
        self.lastDir = path
        self.outpath.setText(self.lastDir)

    def checkShell(self, val, target, func):
        _, value = val
        if not value or value == ShellRunner.SUCCESS or value == ShellRunner.ERROR:
            self.shellRunner.shellRes.disconnect(func)
            return True
        key, _ = val
        if key != target:
            return True
        return False

    def setupScanners(self, scanners: Tuple[str, List[str]]):
        if self.checkShell(scanners, "setupScanners", self.setupScanners):
            return

        _, items = scanners
        self.printerSelect.clear()
        if items:
            self.log("found items:")
            self.logList(items)
            self.printerSelect.addItems(items)
            self.printerSelect.setCurrentIndex(0)
        else:
            self.printerSelect.setEditText("N/A")

    def scan(self):
        if not self.outpath.text():
            self.log("Output path not specified")
            return
        
        self.log("\n==============\n")
        
        targetDir = os.path.join(self.outpath.text(), "scans")
        
        # make output path if not exist
        if not os.path.isdir(targetDir):
            os.makedirs(targetDir)
        
        targetFile = os.path.join(targetDir, f"{self.fileIndex}.jpg")
        while os.path.isfile(targetFile):
            self.fileIndex += 1
            targetFile = os.path.join(targetDir, f"{self.fileIndex}.jpg")

        cmd = f'naps2.console -o "{targetFile}" --noprofile --driver twain --device "{self.printerSelect.currentText()}" --source glass --dpi {self.dpiSelect.currentText()} --pagesize a4 --bitdepth color --jpegquality 100 --progress'
        self.shellRunner.shellRes.connect(self.finishedScan)
        self.shellRunner.queueCommand('scan',cmd, False)
        self.log("Starting Scan...")
        self.scanBtn.setDisabled(True)
        
    
    def finishedScan(self, result : Tuple[str, str]):
        key,val = result
        if key != 'scan':
            return
        self.shellRunner.shellRes.disconnect(self.finishedScan)
        self.setFocus()
        
        # expect no extra message during a good scan
        if val != ShellRunner.SUCCESS:
            self.log("Error occured during scanning")
            return
        
        targetPath = os.path.join(self.outpath.text(), "scans")
        targetFile = os.path.join(targetPath, f"{self.fileIndex}.jpg")
        
        if not os.path.isfile(targetFile):
            return self.log(f"Cannot find scanned file: {targetFile}")
        
        self.log(f"Scan done: {targetFile}")
        self.scanBtn.setEnabled(True)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.shellRunner.terminate()
        return super().closeEvent(a0)

    def log(self, msg: str):
        self.consoleLog.insertPlainText(msg + "\n")

    def logList(self, msgs: List[str]):
        self.log("\n".join(msgs))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    scanner = PhotoScanner()
    sys.exit(a.exec())
