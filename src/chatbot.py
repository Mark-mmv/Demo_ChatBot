import sys
import json
from openai import OpenAI
import settings

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from PyQt5.QtGui import QFont, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QEvent

from interface import Ui_interface_chat_bot


OPENAI_API_KEY = settings.OPENAI_API_KEY


class AIAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.messages = list(dict())
        self.set_system_promt()

    def set_system_promt(self):
        with open("info.txt", "r", encoding="utf-8") as f:
            university_info = f.read()

        system_prompt = f"""
            Jste odborníkem na studijním oddelení Univerzity Karlove v Praze. 
            Odpovězte na otázky POUZE na základě informací uvedených v následujícím textu.:
            {university_info}
            Pokud nejsou k dispozici žádné informace, odpovězte: 
            "Tyto informace nejsou v poskytnutých údajích k dispozici. 
            Mým cílem je zodpovědět dotazy týkající se stipendií na Univerzitě Karlově"
            """

        self.messages: list[dict] = [{"role": "system", "content": system_prompt}]


    def respond(self, messages: list[dict], model: str = "gpt-4o-mini"):
        """
        Vytvoří dotaz na model s úplným seznamem zpráv (historie chatu).
        messages - seznam slovníků tvaru {„role“: „user“ | ‚assistant‘, „content“: „...“}.
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        # Извлекаем текст из ответа
        assistant_message = response.choices[0].message.content
        return assistant_message


class InterfaceMain(QMainWindow, QApplication, Ui_interface_chat_bot):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.assistant = AIAssistant(api_key=OPENAI_API_KEY)

        """Buttons"""
        self.push_button_enter.clicked.connect(self.enter_message)
        self.plain_text_edit.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.plain_text_edit and e.type() == QEvent.KeyPress:
            if e.key() in (Qt.Key_Return, Qt.Key_Enter) and not (e.modifiers() & Qt.ShiftModifier):
                e.accept()
                if not e.isAutoRepeat():
                    self.enter_message()
                return True
        return super().eventFilter(obj, e)

    def input_message(self):
        message = self.plain_text_edit.toPlainText()
        self.print_to_text_browser(message=message, role="User", role_color="#1a7f37", text_color="000000")
        self.assistant.messages.append({"role": "user", "content": message})

    def output_message(self):
        assistant1_reply = self.assistant.respond(self.assistant.messages)
        self.print_to_text_browser(message=assistant1_reply, role="ChatBot", role_color="#d00000", text_color="000000")
        self.assistant.messages.append({"role": "assistant", "content": assistant1_reply})

    def print_to_text_browser(self, message, role="None", role_color="000000", text_color="000000"):
        self.text_browser.setTextColor(QtGui.QColor(f"{role_color}"))
        self.text_browser.append(f"{role}: ")
        self.text_browser.setTextColor(QtGui.QColor(f"{text_color}"))
        self.text_browser.append(f"{message} \n")

    def enter_message(self):
        try:
            self.input_message()
            self.output_message()
            self.plain_text_edit.clear()
        except TimeoutError:
            pass


def main():
    app = QApplication(sys.argv)
    interface_main = InterfaceMain()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
