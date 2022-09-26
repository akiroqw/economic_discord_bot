from config import*

class LevelCard():

    def __init__(self):
        self.level : int = 1
        self.xp : int = 0
        self.required_xp : int = 1
        self.name : str = None
        self.avatar : str = None
        self.color : str = "#1E1E1E"
        self.path : str = None

    async def create(self):
        if self.path != None:
            background = Editor(Canvas((920, 220), color= "#141414"))
            banner = Editor(f"backgrounds/{self.path}").resize((920, 900))
            background.paste(banner, (0, -150)).blur('gussian', 5)
        else:
            background = Editor(Canvas((920, 220), color= "#141414"))

        if(self.avatar != None):
            profile = await load_image_async(str(self.avatar))
            profile = Editor(profile).resize((150, 150)).circle_image()
            background.paste(profile.image, (30, 40))
        else:
            pass
        
        poppins = Font.montserrat(size=40)
        poppins_small = Font.poppins(size=30)

        background.rectangle((200, 145), width=700, height=45, fill="white", radius=20)
        background.bar((200, 145),max_width=700,height=45,percentage= (int(self.xp) / int(self.required_xp)) * 100,fill=self.color,radius=20,)

        if int(self.name.__len__()) > 20:
            self.name = 'Недопустимый ник.'
            background.text((200, 50), str(self.name), font=poppins, color="white")
        else:
            background.text((200, 50), str(self.name), font=poppins, color="white")

        background.text((203, 100),
            f"Level : {int(self.level)}"
            + f"                               XP : {int(self.xp)} / {int(self.required_xp)} EXP",
            font=poppins_small,
            color="white",
        )

        file = File(fp=background.image_bytes, filename="card.png")
        return file