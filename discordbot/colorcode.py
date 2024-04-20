import colorama
import datetime


class cc():
    _init = lambda o: colorama.init()
    RESETf = colorama.Fore.RESET
    RESETb = colorama.Back.RESET
    RESET = '\x1b[0m'+"\x1b[38;2;222;222;222m"
    
    def hexrgbconv(hex):
        if (hex[0] == "#"): hex = hex.lstrip('#')
        else: hex = hex
        return list(int(hex[i:i+2], 16) for i in (0, 2, 4))
    def vFORE(red:int,green:int,blue:int): 
        return f"\x1b[38;2;{red};{green};{blue}m"
    def vBACK(red:int,green:int,blue:int): 
        return f"\x1b[48;2;{red};{green};{blue}m"
    def FORE(hex): 
        x1 = cc.hexrgbconv(hex)
        return cc.vFORE(x1[0],x1[1],x1[2])
    def BACK(hex): 
        x1 = cc.hexrgbconv(hex)
        return cc.vBACK(x1[0],x1[1],x1[2])
    def timeIntro():
        return_ = (cc.FORE('#cc5eff')+'  {:02d}'.format(datetime.datetime.now().hour)+
                cc.FORE("#bbbbbb")+":"+
                cc.FORE('#af5eff')+'{:02d}'.format(datetime.datetime.now().minute)+
                cc.FORE("#bbbbbb")+":"+
                cc.FORE('#995eff')+'{:02d}'.format(datetime.datetime.now().second)+
                cc.FORE("#bbbbbb")+" - ")
        # return " "*2
        return return_

class p():
    def INPUTX(text:str=""):
        der = input(
            cc.timeIntro()+
            cc.RESET+"["+
            cc.FORE("#af3ccf")+"input"+
            cc.RESET+"]: "+
            cc.RESET+text+
            cc.FORE("#ffffff")
        )
        return der
    def PRINTV(text:str="", mode:str='print'):
        stringr = (
                cc.timeIntro()+
                cc.RESET+"["+
                cc.FORE("#b8c8ff")+"info"+
                cc.RESET+"]: "+
                cc.RESET+text
            )
        if (mode == 'print'):
            print(stringr)
        elif (mode == 'text'):
            return stringr
    def PRINTW(text:str="", mode:str='print'):
        stringr = (
                cc.timeIntro()+
                cc.RESET+"["+
                cc.FORE("#fce803")+"welcome"+
                cc.RESET+"]: "+
                cc.RESET+text
            )
        if (mode == 'print'):
            print(stringr)
        elif (mode == 'text'):
            return stringr
    def PRINTX(text:str="", mode:str='print'):
        stringr = (
                cc.timeIntro()+
                cc.RESET+"["+
                cc.FORE("#80fbff")+"log"+
                cc.RESET+"]: "+
                cc.RESET+text
            )
        if (mode == 'print'):
            print(stringr)
        elif (mode == 'text'):
            return stringr
    def PRINTY(text:str="", mode:str='print'):
        stringr = (
                cc.timeIntro()+
                cc.RESET+"["+
                cc.FORE("#96ff96")+"success"+
                cc.RESET+"]: "+
                cc.RESET+text
            )
        if (mode == 'print'):
            print(stringr)
        elif (mode == 'text'):
            return stringr
    def PRINTZ(text:str="", mode:str='print'):
        stringr = (
                cc.timeIntro()+
                cc.RESET+"["+
                cc.FORE("#ff4f4f")+"error"+
                cc.RESET+"]: "+
                cc.RESET+text
            )
        if (mode == 'print'):
            print(stringr)
        elif (mode == 'text'):
            return stringr
