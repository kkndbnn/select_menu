
from email import message
import discord
from discord.ui import Modal, View, button
from discord.ui.input_text import InputText 
from discord.ext.pages import Page, Paginator, PageGroup
from discord.utils import get
from discord.ext import commands
import os


from dotenv import load_dotenv
load_dotenv()

bot = discord.Bot(debug_guilds=[int(os.getenv("GUILD_ID"))])


# pages = [
#     PageGroup(
#         pages=[
#             Page(content="1"),
#             Page(content="2"),
#         ],
#         label="Group 1"
#     ),
#     PageGroup(
#         pages=[
#             Page(content="3"),
#             Page(content="4"),
#             Page(content="5"),
#         ],
#         label="Group 2"
#     )
# ] 


#--------------------------------------------------------
#-----------------------ЗАЯВКА---------------------------
#--------------------------------------------------------


class SurveyModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Подать заявку в семью Ant")

        self.add_item(InputText(
            label="Ник|Статик на Los Angeles|Имя и Возраст",
            placeholder="Konsto Ant | 300 | Константин 19 лет",
            min_length=1,
            max_length=100
        ))

        self.add_item(InputText(
            label="Опыт RP серверов | Ежедневный Онлайн",
            placeholder="Как узнали о нас?",
            min_length=1,
            max_length=100
        ))

        self.add_item(InputText(
            label="В каких семьях состояли?",
            placeholder="По какой причине покинули?",
            min_length=1,
            max_length=100
        ))

        self.add_item(InputText(
            label="Почему выбрали именно нашу фаму?",
            placeholder="Какую пользу сможете принести нашей семье?",
            min_length=1,
            max_length=400
        ))

        self.add_item(InputText(
            style=discord.InputTextStyle.multiline,
            label="Оценка стрельбы",
            placeholder="Откат стрельбы, если нету, то показать себя на деле!",
            min_length=1,
            max_length=400
        ))

#--------------------------------------------------------
#---------------ПЕРЕНАПРАВЛЕНИЕ НА ПРОВЕРКУ--------------
#--------------------------------------------------------


    async def callback(self, intercation: discord.Interaction):
            # name = self.children[0].value
            # exp = self.children[1].value
            # fams = self.children[2].value
            # benefit = self.children[3].value
            # fight = self.children[4].value


            name, exp, fams, benefit, fight = map(lambda x: x.value, self.children)


            channel = bot.get_channel(1249050008511185069) #ID Канала куда поступают заявки
            id_discord = intercation.user.id #ID Пользователя который отправил заявку

            await channel.send(f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ \n <@&1215395955407454240> <@&1215379305698295858> <@&1215379305698295856> \n ***НОВАЯ ЗАЯВКА*** \n \
**Ваш ник | Статик| Имя:** ```{name}``` \
**Ваш опыт и онлайн:** ```{exp}``` **В каких семьях вы были:** ```{fams}``` \
**Почему именно наша семья:** ```{benefit}``` \
**Ваши навыки стрельбы:** \n {fight} \n <@{id_discord}>", view=Button(timeout=None)) #Заявка, с тегом хайранга, и юзера который ее отправил
            
            



            await intercation.response.send_message(embed=discord.Embed(title="Вы успешно подали заявку", description="Ждите сообщение от Бота в ЛС"), ephemeral=True) #фидбэк для пользователя, что заявка отправлена
#--------------------------------------------------------
#--------КОММЕНТАРИЙ К ОТКЛОНЕЕНОЙ ЗАЯВКЕ----------------
#--------------------------------------------------------
class Comment(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Подать заявку в семью Ant")
        self.add_item(InputText(
            style=discord.InputTextStyle.multiline,
            label="Комментарий к заявке",
            placeholder="почему вы откланили?",
            min_length=1,
            max_length=400
        ))
#--------------------------------------------------------
#---------------ПЕРЕНАПРАВЛЕНИЕ В АРХИВ------------------
#--------------------------------------------------------
    async def callback(self, intercation: discord.Interaction):
        comment = self.children[0].value
        id_discord = intercation.user
        id_discord_LS = intercation.user.id
        channel = bot.get_channel(1250619141518397545) #ID канала с архив заявками
        await channel.send(embed = discord.Embed(title="Причина отказа", description=f'{comment} \n <@{id_discord_LS}>', color=0xE74C3C)) #Коментарий к заявке
        #await id_discord.send(embed = discord.Embed(title="Причина отказа", description=f'{comment} \n <@{id_discord_LS}>', color=0xE74C3C))
        await intercation.response.send_message(embed=discord.Embed(title="Вы оставили комментарий", description="Вы оставили комментарий"), ephemeral=True) #фидбэк для проверяющего, что коммент отправлен
        



#--------------------------------------------------------
#--------КНОПКА ПРИНЯТЬ/ОТКЛОНИТЬ ЗАЯВКУ-----------------
#--------------------------------------------------------


class Button(discord.ui.View):
    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, emoji="✔️")
    async def accept_callback(self, button: discord.ui.Button, ctx: discord.ApplicationContext):
        channel = bot.get_channel(1250619141518397545)
        await ctx.message.delete()
        await channel.send(embed = discord.Embed(title="", description=ctx.message.content, image="", color=0x00ff00))
        print(ctx.message.content[-20:-1])


    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.red, emoji="✖️")
    async def reject_callback(self, button: discord.ui.Button, ctx: discord.ApplicationContext):
        channel = bot.get_channel(1250619141518397545)
        await ctx.response.send_modal(Comment())
        await ctx.message.delete()
        await channel.send(embed = discord.Embed(title="", description=ctx.message.content, image="", color=0xE74C3C))


#--------------------------------------------------------
#--------КОМАНДА ВЫЗОВА КНОПКИ ПРИНЯТЬ/ОТКЛОНИТЬ---------
#--------------------------------------------------------
# @bot.command()
# async def feedback(ctx: discord.ApplicationContext):
#     await ctx.send("", view = Button(timeout=None))
#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------



#--------------------------------------------------------
#--------КНОПКА ПОДАТЬ ЗАЯВКУ В СЕМЬЮ--------------------
#--------------------------------------------------------
class MyView(View):
        @button(label="Подать заявку в семью", style=discord.ButtonStyle.green, emoji="📋")
        async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_modal(SurveyModal())
#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------



#--------------------------------------------------------
#--------КОМАНДА ВЫЗОВА КНОПКИ---------------------------
#--------------------------------------------------------
@bot.command()
async def application(ctx: discord.ApplicationContext):
    await ctx.send(embed = discord.Embed(title="", description="", image="https://media1.tenor.com/m/EkvcrALw2SAAAAAC/ant.gif", color=discord.Colour.from_rgb(r=43, g=45, b=49)))
    await ctx.send(embed = discord.Embed(title="Здесь Вы можете подать заявку", description="После заполнения анкеты Вам придет оповещение в ЛС от бота с \n результатом (ответ не придёт, если закрыт \n доступ к сообщениям в discord).", color=discord.Colour.from_rgb(r=43, g=45, b=49)), view=MyView(timeout=None))

#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------




if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
