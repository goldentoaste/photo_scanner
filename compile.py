from PyQt6.uic.compile_ui import compileUi


with open("MainWindow.py", 'w', encoding='utf8') as f:
    compileUi("main.ui", f)