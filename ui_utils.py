import os
from asyncio import run, sleep
from chatGrabber import grabChat
import customtkinter
import pyperclip
from PIL import Image
import asyncio


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.label_list = []
        self.button_list = []

    def add_item(self, label_text, label_image=None, button_image=None):
        label = customtkinter.CTkLabel(self, text=label_text, image=label_image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, image=button_image, fg_color="transparent", text=None, width=20,
                                         height=20)
        button.configure(command=pyperclip.copy(label_text))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.all_players = []

        self.title("Player Recruitment")
        self.geometry("700x450")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "misc.png")), size=(50, 50))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.meets_requirements = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "white_tick.png")), size=(20, 20))
        self.guildless = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_guildless.png")),
                                                size=(20, 15))
        self.dms_enabled = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                  size=(20, 20))
        self.need_to_friend = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.copy_icon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_copy.png")),
                                                size=(20, 20))
        self.settings_icon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_settings_icon.png")),
                                                    size=(20, 20))
        self.iconbitmap(os.path.join(image_path, "misc.ico"))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Player Recruitment",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)


        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="All",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew", columnspan=2)

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Meets Requirements",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.meets_requirements, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew", columnspan=2)

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Guildless & Meets Requirements",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.guildless, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew", columnspan=2)

        self.find_players_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, border_spacing=5,
                                                      text="Find Players", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      command=self.find_players_button_event)
        self.find_players_button.grid(row=5, column=0, padx=15, pady=15,sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, image=self.settings_icon, fg_color="transparent", text=None, width=20,
                                                        height=20)
        self.settings_button.grid(row=5, column=1, padx=5)




        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.home_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
        self.home_frame_no_players_label = customtkinter.CTkLabel(self.home_frame,
                                                                  text="No players found.\nPlease run /list in a lobby",
                                                                  font=customtkinter.CTkFont(size=30, weight="bold"))
        self.home_frame_no_players_label.place(relx=0.5, rely=0.5, anchor="center")
        # self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.home_frame.grid_columnconfigure(0, weight=1)
        # self.home_frame_text_box = customtkinter.CTkTextbox(self.home_frame, activate_scrollbars=True)
        # self.home_frame_text_box.grid(row = 1, column = 0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame_no_players_label = customtkinter.CTkLabel(self.second_frame,
                                                                    text="No players found.\nPlease run /list in a lobby",
                                                                    font=customtkinter.CTkFont(size=30, weight="bold"))
        self.second_frame_no_players_label.place(relx=0.5, rely=0.5, anchor="center")

        # create third frame
        # self.third_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame_no_players_label = customtkinter.CTkLabel(self.third_frame,
                                                                   text="No players found.\nPlease run /list in a lobby",
                                                                   font=customtkinter.CTkFont(size=30, weight="bold"))
        self.third_frame_no_players_label.place(relx=0.5, rely=0.5, anchor="center")
        # select default frame
        self.select_frame_by_name("home")


    def find_players(self):
        all_players, guildless, meets_requirements = asyncio.run(grabChat())
        if all_players is not None and set(all_players) != set(self.all_players):
            #self.home_frame.grid_forget()
            #self.home_frame.destroy()
            self.home_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in all_players:
                if player:
                    self.home_frame.add_item(label_text=player, button_image=self.copy_icon)

            #self.second_frame.grid_forget()
            #self.second_frame.destroy()
            self.second_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in meets_requirements:
                if player:
                    self.second_frame.add_item(label_text=player, button_image=self.copy_icon)

            #self.third_frame.grid_forget()
            self.third_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in guildless:
                if player:
                    self.third_frame.add_item(label_text=player, button_image=self.copy_icon)

        self.all_players = all_players


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def find_players_button_event(self):
        self.find_players()