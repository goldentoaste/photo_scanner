import os
import subprocess
import sys
from math import sqrt
from time import sleep
from typing import List, Tuple

import cv2
import numpy as np
from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget

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
        self.shellRunner.queueCommand("scan", cmd, False)
        self.log("Starting Scan...")
        self.scanBtn.setDisabled(True)

    def finishedScan(self, result: Tuple[str, str]):
        key, val = result
        if key != "scan":
            return
        self.shellRunner.shellRes.disconnect(self.finishedScan)
        self.setFocus()

        # expect no extra message during a good scan
        if val != ShellRunner.SUCCESS:
            self.log("Error occured during scanning")
            self.scanBtn.setEnabled(True)

            return

        targetPath = os.path.join(self.outpath.text(), "scans")
        targetFile = os.path.join(targetPath, f"{self.fileIndex}.jpg")

        if not os.path.isfile(targetFile):
            return self.log(f"Cannot find scanned file: {targetFile}")

        self.log(f"Scan done: {targetFile}")
        self.processImage(targetFile)
        self.scanBtn.setEnabled(True)

    def crop_minAreaRect(self, img, rect):
        # https://stackoverflow.com/a/43099932/12471420
        # Thanks!

        rows, cols = img.shape[0], img.shape[1]
        diag = int(sqrt(rows * rows + cols * cols))
        newimg = np.zeros((diag, diag, 3), dtype=np.uint8)

        rowsOffset = (diag - rows) // 2
        colsOffset = (diag - cols) // 2

        newimg[rowsOffset : rowsOffset + rows, colsOffset : colsOffset + cols] = img
        img = newimg
        # rotate img
        angle = rect[2]
        M = cv2.getRotationMatrix2D((diag / 2, diag / 2), angle, 1)
        img_rot = cv2.warpAffine(img, M, (diag, diag))

        # rotate bounding box
        rect0 = ((rect[0][0] + colsOffset, rect[0][1] + rowsOffset), rect[1], angle)
        box = cv2.boxPoints(rect0)
        pts = np.intp(cv2.transform(np.array([box]), M))[0]  # type: ignore
        pts[pts < 0] = 0

        # crop
        img_crop = img_rot[pts[1][1] : pts[0][1], pts[1][0] : pts[2][0]]

        return img_crop

    def processImage(self, imgPath: str):
        self.log("scan complete, now finding photos.")
        img = cv2.imread(imgPath)
        blur = cv2.pyrMeanShiftFiltering(img, 11, 21)

        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 230, 225, cv2.THRESH_BINARY_INV)

        conts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        conts = conts[0] if len(conts) == 2 else conts[1]

        good = []
        for c in conts:
            rotatedRect = cv2.minAreaRect(c)
            minRectPoints = cv2.boxPoints(rotatedRect)
            a = rotatedRect[1][0]
            b = rotatedRect[1][1]

            if cv2.contourArea(minRectPoints, False) > 6000 and (a / b <= 3 and b / a < 3):
                print(rotatedRect)
                good.append(self.crop_minAreaRect(img, self.fixRotRect(rotatedRect)))  # type: ignore

        self.log(f"Found {len(good)} images. showing preview for all of them now.")
        for g in good:
            print(g.shape)
            cv2.imshow("yeah", cv2.resize(g, (600, int(600 * g.shape[0] / g.shape[1])) ))
            cv2.waitKey()
        cv2.destroyAllWindows()
        self.saveSubImages(good)

    def saveSubImages(self, imgs):
        targetPath = self.outpath.text()
        idx = 0
        
        for img in imgs:
            cv2.imwrite(os.path.join(targetPath, f"{self.fileIndex}_{idx}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            self.log(f"Saved {os.path.join(targetPath, f"{self.fileIndex}_{idx}.jpg")}")
            idx += 1

    def fixRotRect(self, rect):
        if rect[2] > 45:
            return (rect[0], (rect[1][1], rect[1][0]), rect[2] - 90)

        if rect[2] < -45:
            return (rect[0], (rect[1][1], rect[1][0]), rect[2] + 90)

        return rect

    def _processImage(self, imgPath: str):
        img = cv2.imread(imgPath)
        blur = cv2.pyrMeanShiftFiltering(img, 11, 21)

        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 230, 225, cv2.THRESH_BINARY_INV)

        cv2.imshow("img", binary)

        conts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        conts = conts[0] if len(conts) == 2 else conts[1]

        good = []
        for c in conts:
            rotatedRect = cv2.minAreaRect(c)
            minRectPoints = cv2.boxPoints(rotatedRect)
            minRect = np.intp(minRectPoints)

            a = rotatedRect[1][0]
            b = rotatedRect[1][1]
            if cv2.contourArea(minRectPoints, False) > 6000 and (a / b <= 3 and b / a < 3):
                good.append(minRect)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.shellRunner.terminate()
        return super().closeEvent(a0)

    def log(self, msg: str):
        self.consoleLog.insertPlainText(msg + "\n")

    def logList(self, msgs: List[str]):
        self.log("\n".join(msgs))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    s = PhotoScanner()
    sys.exit(a.exec())
