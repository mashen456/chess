from stockfish import Stockfish
from cfg.cfg import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import random

movelist = []

stockfish = Stockfish(STOCKFISH_PATH)


def get_play(driver):
    f = ' '
    t = ' '
    for x in range(8):
        for y in range(8):
            letter = 'abcdefgh'
            try:

                field = letter[x] + str(y + 1)
                item = driver.find_element(By.XPATH, '//*[@id="' + field + '"]').get_attribute('class')
                if str(item).find('moved') != -1:
                    try:
                        sitem = driver.find_element(By.XPATH, '//*[@id="' + field + '"]/div[2]')
                        f = field
                    except:
                        t = field


            except:
                None
    return t+f


def get_color():
    c = input('1 If you are white 2 if you are black\n')
    if c == '1':
        return 'white'
    if c == '2':
        return 'black'

def init_driver(link):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1900x1000")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    driver.get('http://www.schach-spielen.eu/game/' +link)
    return driver


def playg(driver):
    p = get_play(driver)
    movelist.append(p)
    stockfish.set_position(movelist)
    bm = stockfish.get_best_move()
    moove(driver,bm)
    movelist.append(bm)

def moove(driver,move):

    element = driver.find_element(By.XPATH,'//*[@id="' +move[0:2]+'"]')
    element.click()
    time.sleep(random.randrange(1,3,1))
    element =driver.find_element(By.XPATH,'//*[@id="'+move[2:4]+'"]')
    element.click()

def main():
    driver = init_driver(input('Lobby code : \n'))
    a = input('Enter when ready')
    if get_color() == 'white':
        print('you are white')
        fmove = stockfish.get_best_move()
        moove(driver,fmove)
        moove(driver,fmove)
        movelist.append(fmove)
    else:
        print('you are black')
        play = get_play(driver)
        movelist.append(play)
        stockfish.set_position(movelist)
        fmove = stockfish.get_best_move()
        moove(driver, fmove)
        movelist.append(fmove)

    while True:
        k = input('Enter to play')
        playg(driver)




main()




