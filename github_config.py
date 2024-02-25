import sys
import subprocess
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QProgressBar, QRadioButton, QButtonGroup)
from PyQt5.QtCore import pyqtSlot

class GitConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Git Configurator')
        self.setGeometry(100, 100, 450, 350)

        layout = QVBoxLayout()

        self.githubAccountLabel = QLabel('GitHub Account:', self)
        layout.addWidget(self.githubAccountLabel)

        self.githubAccountInput = QLineEdit(self)
        layout.addWidget(self.githubAccountInput)

        self.sshKeyOptionLabel = QLabel('SSH Key Handling:', self)
        layout.addWidget(self.sshKeyOptionLabel)

        self.manualKeyRadio = QRadioButton("Manually Enter SSH Key")
        self.apiKeyRadio = QRadioButton("Automatically Generate via GitHub API")
        self.manualKeyRadio.setChecked(True)  # Default to manual entry
        self.radioGroup = QButtonGroup(self)
        self.radioGroup.addButton(self.manualKeyRadio)
        self.radioGroup.addButton(self.apiKeyRadio)
        layout.addWidget(self.manualKeyRadio)
        layout.addWidget(self.apiKeyRadio)

        self.sshKeyInput = QLineEdit(self)
        self.sshKeyInput.setPlaceholderText("Enter your SSH key here if manually handling SSH keys")
        layout.addWidget(self.sshKeyInput)

        self.statusWindow = QTextEdit(self)
        self.statusWindow.setReadOnly(True)
        layout.addWidget(self.statusWindow)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        layout.addWidget(self.progressBar)

        self.checkConfigButton = QPushButton('Check Current Configuration', self)
        self.checkConfigButton.clicked.connect(self.checkCurrentConfig)
        layout.addWidget(self.checkConfigButton)

        self.runButton = QPushButton('Run', self)
        self.runButton.clicked.connect(self.runConfiguration)
        layout.addWidget(self.runButton)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.cancelOperation)
        layout.addWidget(self.cancelButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def checkCurrentConfig(self):
        self.updateProgress(0)
        threading.Thread(target=self.executeGitCommand, args=('git config --list',), daemon=True).start()

    def runConfiguration(self):
        self.statusWindow.append("Starting configuration...")
        # Implement the configuration process in steps, updating progress accordingly
        # This is a placeholder for the actual implementation
        for i in range(1, 101):
            self.updateProgress(i)
            threading.Thread(target=self.dummyProcess, args=(i,), daemon=True).start()

    def cancelOperation(self):
        self.statusWindow.append("Program Canceled")
        self.updateProgress(0)

    def executeGitCommand(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            self.updateStatusWindow(output)
        except subprocess.CalledProcessError as e:
            self.updateStatusWindow(str(e.output))

    def updateStatusWindow(self, text):
        if self.statusWindow:
            self.statusWindow.append(text)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def dummyProcess(self, value):
        # Simulate a process
        pass

def main():
    app = QApplication(sys.argv)
    ex = GitConfigurator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
