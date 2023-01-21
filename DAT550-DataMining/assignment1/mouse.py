import pyautogui as pag

w,h = pag.size()
y = 100
while True:
    pag.moveRel(0, y, duration = 1)
    y = -y
