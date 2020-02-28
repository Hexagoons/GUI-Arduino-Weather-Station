from dashboard.views import *
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


class Application(ThemedTk):
    """
    Hanzehogeschool Groningen University of Applied Sciences HBO-ICT
    Project Computer Systems 2.1
    De Centrale

    :author Roy Voetman
    :author Joey Marthé Behrens
    :author Robin van Wijk
    :author Shaquille Louisa
    """
    def __init__(self):
        # Create tkinter window
        ThemedTk.__init__(self, theme="arc")

        self.title("De Centrale")

        # Sub dir needed for pass by reference
        self.connected = {'devices': {}}

        # Creating the view container
        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill='both', side='right')

        # Set resizeable weights per column
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create all views
        self.views = {
            'Dashboard': self.create_view(Dashboard),
            'Settings': self.create_view(Settings)
        }

        # Create the sidebar
        self.build_sidebar()

        # Start at Dashboard
        self.show_view('Dashboard')

    def create_view(self, view):
        """
        Creates view class based on fully qualified class name
        :param view: Fully qualified class name
        :return: View object
        """
        view = view(self.container, self.connected)

        view.grid(row=0, column=0, sticky="nsew")

        return view

    def build_sidebar(self):
        """
        Build the sidebar frame
        """
        sidebar = ttk.Frame(self, relief='ridge', borderwidth=2)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        # Resize and attach logo
        image = Image.open("logo.jpg")
        size = 35, 35
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(sidebar, image=photo)
        label.image = photo  # keep a reference other wise image will be removed
        label.pack(fill=tk.X)

        # View buttons
        button1 = ttk.Button(sidebar, text="Dashboard", width=15, command=lambda: self.show_view('Dashboard'))
        button1.pack(fill=tk.X, pady=10)
        
        button2 = ttk.Button(sidebar, text="Settings", width=15, command=lambda: self.show_view('Settings'))
        button2.pack(fill=tk.X, pady=10)

    def show_view(self, container):
        """
        Raise a specific view
        :param container: View name
        """
        view = self.views[container]
        view.OpenView()
