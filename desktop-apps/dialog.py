from PyQt5.QtWidgets import QDialog, QMessageBox

class Dialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("¿Seguro que desea borrar?")
        self.setFixedSize(400, 200)
        self.ask_for_confirmation()
        
    def ask_for_confirmation(self):

		answer = QMessageBox.question(self, "Confirm closing",
					"You have unsaved changes. Are you sure you want to exit?", 
					QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
		return answer