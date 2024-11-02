from enum import Enum

class HandValue(Enum):
    HV00 = "https://cdn.discordapp.com/attachments/886007452997386273/1302218772878327818/00.png"
    HV01 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039640953458780/01.png"
    HV02 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039641352044595/02.png"
    HV03 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039641691783229/03.png"
    HV04 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039641943310436/04.png"
    HV05 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039642421330040/05.png"
    HV06 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039742514331729/06.png"
    HV07 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039742824845323/07.png"
    HV08 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039743084630016/08.png"
    HV09 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039743487541268/09.png"
    HV10 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039744007372884/10.png"
    HV11 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039764446216193/11.png"
    HV12 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039764693946408/12.png"
    HV13 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039764899201087/13.png"
    HV14 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039765134086194/14.png"
    HV15 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039765394260058/15.png"
    HV16 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039779084603442/16.png"
    HV17 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039779403235358/17.png"
    HV18 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039779617017977/18.png"
    HV19 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039779990442015/19.png"
    HV20 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039780225318942/20.png"
    HV21 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039795593379850/21.png"
    HV22 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039795819876352/22.png"
    HV23 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039796079661086/23.png"
    HV24 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039796411269152/24.png"
    HV25 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039796625182771/25.png"
    HV26 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039811728867448/26.png"
    HV27 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039811925872660/27.png"
    HV28 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039812152360971/28.png"
    HV29 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039812337041500/29.png"
    HV30 = "https://cdn.discordapp.com/attachments/886007452997386273/1302039812634710167/30.png"

    @classmethod
    def from_int(cls, value: int):
        try:
            member_name = f"HV{value:02}"
            return getattr(cls, member_name).value
        except AttributeError:
            return None
