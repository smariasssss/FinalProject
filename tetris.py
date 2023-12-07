import pygame as pg  # Импорт библиотеки Pygame для создания игры
import random, time, sys  # Импорт модулей для случайных чисел, времени и системных функций
from pygame.locals import *  # Импорт различных констант и функций из Pygame

fps = 25  # Частота кадров в секунду для игры
window_w, window_h = 600, 500  # Ширина и высота окна игры
block, cup_h, cup_w = 20, 20, 10  # Размеры блока и стакана для игрового поля

side_freq, down_freq = 0.15, 0.1  # Частота передвижения фигур в сторону и вниз

side_margin = int((window_w - cup_w * block) / 2)  # Отступ от края окна до стакана
top_margin = window_h - (cup_h * block) - 5  # Отступ сверху до стакана

colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # Цвета для фигур: синий, зеленый, красный, желтый
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))  # Светлые оттенки цветов фигур

white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)  # Определение основных цветов
brd_color, bg_color, txt_color, title_color, info_color = white, black, white, colors[3], colors[0]  # Цвета интерфейса

fig_w, fig_h = 5, 5  # Размеры фигур для игры
empty = 'o'  # Символ для обозначения пустого места на игровом поле

# Словарь фигур: каждая фигура представлена матрицей символов, описывающих ее форму
figures = {
    'S': [  # Фигура S (зеленая)
        ['ooooo',  # Поворот 1
         'ooooo',
         'ooxxo',
         'oxxoo',
         'ooooo'],
        ['ooooo',  # Поворот 2
         'ooxoo',
         'ooxxo',
         'oooxo',
         'ooooo']
    ],
    'Z': [  # Фигура Z (красная)
        ['ooooo',  # Поворот 1
         'ooooo',
         'oxxoo',
         'ooxxo',
         'ooooo'],
        ['ooooo',  # Поворот 2
         'ooxoo',
         'oxxoo',
         'oxooo',
         'ooooo']
    ],
    'J': [  # Фигура J (синяя)
        ['ooooo',  # Поворот 1
         'oxooo',
         'oxxxo',
         'ooooo',
         'ooooo'],
        ['ooooo',  # Поворот 2
         'ooxxo',
         'ooxoo',
         'ooxoo',
         'ooooo'],
        ['ooooo',  # Поворот 3
         'ooooo',
         'oxxxo',
         'oooxo',
         'ooooo'],
        ['ooooo',  # Поворот 4
         'ooxoo',
         'ooxoo',
         'oxxoo',
         'ooooo']
    ],
    'L': [  # Фигура L (оранжевая)
        ['ooooo',  # Поворот 1
         'oooxo',
         'oxxxo',
         'ooooo',
         'ooooo'],
        ['ooooo',  # Поворот 2
         'ooxoo',
         'ooxoo',
         'ooxxo',
         'ooooo'],
        ['ooooo',  # Поворот 3
         'ooooo',
         'oxxxo',
         'oxooo',
         'ooooo'],
        ['ooooo',  # Поворот 4
         'oxxoo',
         'ooxoo',
         'ooxoo',
         'ooooo']
    ],
    'I': [  # Фигура I (желтая)
        ['ooxoo',  # Поворот 1
         'ooxoo',
         'ooxoo',
         'ooxoo',
         'ooooo'],
        ['ooooo',  # Поворот 2
         'ooooo',
         'xxxxo',
         'ooooo',
         'ooooo']
    ],
    'O': [  # Фигура O (фиолетовая)
        ['ooooo',  # Поворот 1
         'ooooo',
         'oxxoo',
         'oxxoo',
         'ooooo']
    ],
    'T': [  # Фигура T (красная)
        ['ooooo',  # Поворот 1
         'ooxoo',
         'oxxxo',
         'ooooo',
         'ooooo'],
        ['ooooo',  # Поворот 2
         'ooxoo',
         'ooxxo',
         'ooxoo',
         'ooooo'],
        ['ooooo',  # Поворот 3
         'ooooo',
         'oxxxo',
         'ooxoo',
         'ooooo'],
        ['ooooo',  # Поворот 4
         'ooxoo',
         'oxxoo',
         'ooxoo',
         'ooooo']
    ]
}


def pauseScreen():
    # Создание экрана паузы
    pause = pg.Surface((600, 500), pg.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    display_surf.blit(pause, (0, 0))


def main():
    # Основная функция игры
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((window_w, window_h))
    basic_font = pg.font.SysFont('arial', 20)
    big_font = pg.font.SysFont('verdana', 45)
    pg.display.set_caption('Тетрис Lite')
    showText('Тетрис Lite')  # Выводит на экран название игры
    while True:  # Начинает игру
        runTetris()  # Запускает функцию Tetris
        pauseScreen()  # Показывает экран паузы
        showText('Игра закончена')  # Выводит сообщение об окончании игры


def runTetris():
    # Основная функция Tetris
    cup = emptycup()  # Создает пустой стакан
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calcSpeed(points)  # Вычисляет уровень и скорость падения фигур
    fallingFig = getNewFig()  # Получает новую фигуру
    nextFig = getNewFig()  # Получает следующую фигуру

    while True:
        if fallingFig == None:
            # если нет падающих фигур, генерируем новую
            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time.time()

            if not checkPos(cup, fallingFig):
                return  # если на игровом поле нет свободного места - игра закончена
        quitGame()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pauseScreen()
                    showText('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                # перемещение фигуры вправо и влево
                if event.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_left or going_right) and time.time() - last_side_move > side_freq:
            if going_left and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
            elif going_right and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > down_freq and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:  # свободное падение фигуры
            if not checkPos(cup, fallingFig, adjY=1):  # проверка "приземления" фигуры
                addToCup(cup, fallingFig)  # фигура приземлилась, добавляем ее в содержимое стакана
                points += clearCompleted(cup)
                level, fall_speed = calcSpeed(points)
                fallingFig = None
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                fallingFig['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        display_surf.fill(bg_color)
        drawTitle()
        gamecup(cup)
        drawInfo(points, level)
        drawnextFig(nextFig)
        if fallingFig != None:
            drawFig(fallingFig)
        pg.display.update()
        fps_clock.tick(fps)


def txtObjects(text, font, color):
    # Создает текстовую поверхность и возвращает ее вместе с ее прямоугольной областью
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stopGame():
    # Останавливает игру, завершает Pygame и выходит из системы
    pg.quit()
    sys.exit()


def checkKeys():
    # Проверяет нажатие клавиш
    quitGame()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showText(text):
    # Выводит текст на экран и ждет нажатия клавиши
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
    display_surf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = txtObjects('Нажмите любую клавишу для продолжения', basic_font, title_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checkKeys() == None:
        pg.display.update()
        fps_clock.tick()


def quitGame():
    # Проверяет события, приводящие к выходу из игры
    for event in pg.event.get(QUIT):
        stopGame()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stopGame()
        pg.event.post(event)


def calcSpeed(points):
    # Вычисляет уровень и скорость падения фигур в зависимости от очков
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def getNewFig():
    # Возвращает новую фигуру со случайными параметрами
    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(cup_w / 2) - int(fig_w / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return newFigure


def addToCup(cup, fig):
    # Добавляет фигуру в стакан
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def emptycup():
    # Создает пустой стакан
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup


def incup(x, y):
    # Проверяет, находится ли координата внутри стакана
    return x >= 0 and x < cup_w and y < cup_h


def checkPos(cup, fig, adjX=0, adjY=0):
    # Проверяет, находится ли фигура в пределах стакана и не пересекается ли с другими фигурами
    for x in range(fig_w):
        for y in range(fig_h):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True


def isCompleted(cup, y):
    # Проверяет, содержит ли ряд в стакане только заполненные блоки
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True


def clearCompleted(cup):
    # Удаляет полностью заполненные ряды из стакана и сдвигает верхние ряды вниз
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if isCompleted(cup, y):
            for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convertCoords(block_x, block_y):
    # Конвертирует координаты блока в пиксели
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    # Рисует блок в указанных координатах
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pg.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pg.draw.circle(display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)


def gamecup(cup):
    # Отрисовывает игровой стакан и его фон
    pg.draw.rect(display_surf, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8),
                 5)

    pg.draw.rect(display_surf, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h))
    for x in range(cup_w):
        for y in range(cup_h):
            drawBlock(x, y, cup[x][y])


def drawTitle():
    # Отображает название игры в верхнем углу окна
    titleSurf = big_font.render('Тетрис Lite', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (window_w - 425, 30)
    display_surf.blit(titleSurf, titleRect)


def drawInfo(points, level):
    # Отображает информацию о баллах, уровне и управлении на экране
    pointsSurf = basic_font.render(f'Баллы: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 550, 180)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 550, 250)
    display_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_w - 550, 420)
    display_surf.blit(pausebSurf, pausebRect)

    escbSurf = basic_font.render('Выход: Esc', True, info_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (window_w - 550, 450)
    display_surf.blit(escbSurf, escbRect)


def drawFig(fig, pixelx=None, pixely=None):
    # Отрисовывает фигуру на поле
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


def drawnextFig(fig):  # Превью следующей фигуры
    nextSurf = basic_font.render('Следующая:', True, txt_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 150, 180)
    display_surf.blit(nextSurf, nextRect)
    drawFig(fig, pixelx=window_w - 150, pixely=230)


if __name__ == '__main__':
    main()
