from multiprocessing import Process
from building_main import run_telebot
from building_main import run_pyrogram

if __name__ == '__main__':

    p1 = Process(target=run_telebot,  daemon=True)
    p2 = Process(target=run_pyrogram, daemon=True)

    p2.start()
    p1.start()
    p1.join()
    p2.join()

