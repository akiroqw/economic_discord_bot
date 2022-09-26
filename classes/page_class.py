
from config import*

class Page(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0
        self.prev_page.disabled = True
        self.next_page.disabled = False

        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")
            
    @discord.ui.button(label ="Previous Page", style=discord.ButtonStyle.secondary)
    async def prev_page(self, interaction: discord.MessageInteraction, button: discord.ui.Button):
        self.embed_count -= 1
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        if self.embed_count == 0:
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.MessageInteraction, button: discord.ui.Button):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]

        self.prev_page.disabled = False

        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)
