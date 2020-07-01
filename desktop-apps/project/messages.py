from PyQt5.QtWidgets import QMessageBox


class Message(QMessageBox):
    
    def __init__(self):
        super().__init__()


    def show_about_dialog(self):
        text = """
			<center> <h1>PyFileBrowser</h1></center>
			<p>Version 1.0.0</p>
			<p>Created by <a href="https://twiter.com/RoberHerraiz">@RoberHerraiz</a>.</p>
		    """
        
        self.about(None, "PyFileBrowser", text)


    def ask_for_confirmation(self):

        ''' Prevents leaving without saving '''

        answer = QMessageBox.question(None, "Confirm closing",
                    "You have unsaved changes. Are you sure you want to exit?", 
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        return answer


    def ask_for_delete_confirmation(self, filename):

        ''' Raise a warning popup asking for confirmation for deleting 
        recursively a directory and all it's files '''

        answer = QMessageBox.warning(None, "Confirm delete",
                f"This folder isn't empty.\n\nAre you sure you want to delete the folder and all the files?\n\nThe folder is: '{filename}'", 
                QMessageBox.Yes | QMessageBox.Cancel)

        return answer


    def unicode_decode_error(self):

        """ Raise an information pop-up reporting that the binary file
        can't be decoded."""

        QMessageBox.information(None, "We can't open the file",
            "The selected file is binary and cannot be decoded ", 
            QMessageBox.Ok)