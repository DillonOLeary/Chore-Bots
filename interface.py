from tkinter import *
from tkinter.ttk import Frame, Button, Style


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.style = Style()
        self.style.theme_use("default")

        self.master.title("Quit button")
        self.pack(fill=BOTH, expand=1)
        frame = Frame(self)
        frame.pack()
        Lb1 = Listbox(frame, relief="sunken")
        Lb1.insert(1, "Robo1")
        Lb1.insert(2, "Robo2")
        Lb1.insert(3, "Robo3")

        Lb1.pack(side=LEFT, padx=10, pady=10,
                 ipadx=10, ipady=10)
        Lb2 = Listbox(frame, relief="sunken", state=DISABLED)
        Lb2.insert(1, "TASK1")
        Lb2.insert(2, "TASK2")
        Lb2.insert(3, "TASK3")
        Lb2.insert(4, "TASK4")
        Lb2.insert(5, "TASK5")
        Lb2.insert(6, "TASK6")

        Lb2.pack(side=RIGHT, padx=10, pady=10,
                 ipadx=10, ipady=10)
        quitButton = Button(self, text="Quit",
                            command=self.quit)
        quitButton.pack(side=BOTTOM, padx=10, pady=10,
                        ipadx=10, ipady=10)


def main():
    root = Tk()
    root.geometry("600x500+200+50")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()