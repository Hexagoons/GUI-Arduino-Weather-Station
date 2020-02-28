from dashboard.Application import Application

if __name__ == "__main__":
    app = Application()
    app.geometry("640x450")
    app.resizable(False, False)

    while True:
        try:
            app.mainloop()
        except UnicodeDecodeError as e:
            pass
