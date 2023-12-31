import random
import os  # для os.system('cls')

class BattleShipExc(Exception):
    def __init__(self, message='Что-то не так', ext_i=''):
        super().__init__(message)
        self.extra_info = ext_i


class Board:
    """! Только для версии python 3.7 и выше, иначе словарь будет неупорядоченным!

    """
    def __init__(self, hide=True):
        self.lst_s = ['a', 'b', 'c', 'd', 'e', 'f']
        self.lst_n = range(1, 7)
        self.keys = [f'{c}{n}' for n in self.lst_n for c in self.lst_s]  # Список координат поля.
        # !! только для версии python 3.7 и выше! иначе словарь будет неупорядоченным.
        self._b_p = {k: ' ' for k in self.keys}  # поле игрока
        self._b_ai = {k: ' ' for k in self.keys}  # поле аи
        self.id_key = {i: k for i, k in enumerate(self.keys)}  # словарь для ИИ. По id будет получать координаты.
        self.values = ['□', '◦', '◌', '◙', ' ', '■']
        self.hide = hide  # Метод, который выводит доску в консоль в зависимости от параметра hid.

    @property
    def b_p(self):
        return self._b_p

    @b_p.setter
    def b_p(self, value):
        if value[0] in self.keys:
            if value[1] in self.values:
                self._b_p[value[0]] = value[1]
            else:
                raise BattleShipExc(ext_i=f'{value[1]}', message=f'Введены неправильный символ ({value[1]})')
        else:
            raise BattleShipExc(ext_i=f'{value[0]}', message=f'Введены неправильные координаты ({value[0]})')

    @property
    def b_ai(self):
        return self._b_ai

    @b_ai.setter
    def b_ai(self, value):
        if value[0] in self.keys:
            if value[1] in self.values:
                self._b_ai[value[0]] = value[1]
            else:
                raise BattleShipExc()
        else:
            raise BattleShipExc()

    def show_board(self, shooter=None, last_shot_info=None):
        os.system('cls')  # !! работает в pycharm, только если включить эмуляцию python консоли. Сделать это можно на панели Run в настройках кликнув на значок ключа под значком треугольника 'play'. Затем в Execution поставить галочку напротив "Emulate terminal in output console". В эти настройки также можно попасть через зажатие (Shift Alt F10).
        #!! По началу пытался принтовать по типу :print(f'1 | {b_p["a1"]} | {b_p["b1"]} | {b_p["c1"] и тд....
        # цикл и генераторы оказались быстрее на 30% в среднем.
        # Если прочли это, не могли бы подсказать. Это из-за того что генераторы не нагружают память, а выдают только необходимое значение в данной итерации?
        print(f"        Ваше поле                                     Поле противника    ")
        print(f'    A   B   C   D   E   F                          A   B   C   D   E   F  ')
        for i in range(6):
            t = f'{i + 1} ' + \
                  ''.join([f'| {x} ' for x in list(self.b_p.values())][6 * i:6 * (i + 1)]) + \
                  '|' + self.emodzi(i, shooter=shooter, last_shot_info=last_shot_info) + f'{i + 1} ' + \
                  self.show_line(i) + '|'
            print(t)


    def emodzi(self, i, shooter=None, last_shot_info=None):
        ai_misses = ['(≖_≖ )', '(╥﹏╥)', 'ಥ_ಥ ']
        pl_misses = ['(─‿‿─)', ' (•◡•) /']

        ai_hits = ['ᕙ(`▿´)ᕗ ', 'ᕙ(^▿^-ᕙ)', "(ง︡'-'︠)ง ", '¯\_( ͡`‿‿ ͡´)_/¯']
        pl_hits = ['٩(×̯×)۶ ', '( ˘︹˘ )', '(҂`︹´)ᕤ']

        ai_dead = ['(҂︠︹ ︡´)ᕤ', 'ᕙ(•︡益︠•ᕙ ) ', 't( ͡`︹ ͡´t)']
        pl_dead = ['(•︡益︠•)', '¯\_( ͡`‿‿ ͡´)_/¯']

        text = ' ' * 20
        if not shooter:
            return text
        else:
            if i in [0, 1, 5]:
                return text
            elif i == 3:
                text = "  <- - - - - - - -  " if shooter == 'ai' else "  - - - - - - - ->  "

            elif i == 4:
                if shooter == 'ai':
                    if last_shot_info == 0:
                        text = '    ИИ промазал     '
                    if last_shot_info == 1:
                        text = '       Ранен!       '
                    if last_shot_info == 2:
                        text = '      Потоплен!!    '
                else:
                    if last_shot_info == 0:
                        text = '   Игрок промазал   '
                    if last_shot_info == 1:
                        text = '       Ранен!       '
                    if last_shot_info == 2:
                        text = '      Потоплен!!    '

            else:
                if shooter == 'ai':
                    if last_shot_info == 0:
                        em = random.choice(ai_misses)
                    elif last_shot_info == 1:
                        em = random.choice(ai_hits)
                    elif last_shot_info == 2:
                        em = random.choice(pl_dead)
                    else:
                        em = '(─‿‿─)'
                else:
                    if last_shot_info == 0:
                        em = random.choice(pl_misses)
                    elif last_shot_info == 1:
                        em = random.choice(pl_hits)
                    elif last_shot_info == 2:
                        em = random.choice(ai_dead)
                    else:
                        em = '(─‿‿─)'

                space = int((20 - len(em))/2)
                text = ' ' * space + em + ' ' * space
        return text




    def show_line(self, i):
        t_a_i = ''

        for cell in list(self.b_ai.values())[6 * i:6 * (i + 1)]:
            if self.hide:
                if cell in [' ', '□']:
                    cell = '◦'
            t_a_i += f'| {cell} '
        return t_a_i

    def cont_id(self, c_cord, step_lst, c_cords, for_dead):  # возвращает словарь из 1 координаты и 1 тела
            d = {}
            cell_i = self.keys.index(c_cord)
            cnt_str = '◌' if for_dead else '◦'
            for step in step_lst:
                i = cell_i + step
                if 0 <= i <= 35:
                    coord = self.keys[i]
                    if coord not in c_cords:
                        d[coord] = cnt_str
            return d

    def contour(self, body, for_dead=False):  # принимает словарь тела корабля
        # возвращает словарь контура вокруг корабля
        c_cords = body.keys()
        d = {}

        for c_cord, cell in body.items():
            corner = ['a1', 'f1', 'a6', 'f6']
            if c_cord in corner:  # если клетка корабля в углу
                if c_cord == 'a1':
                    d.update(self.cont_id(c_cord, [1, 6, 7], c_cords, for_dead))
                if c_cord == 'f1':
                    d.update(self.cont_id(c_cord, [-1, 6, 5], c_cords, for_dead))
                if c_cord == 'a6':
                    d.update(self.cont_id(c_cord, [1, -6, -5], c_cords, for_dead))
                if c_cord == 'f6':
                    d.update(self.cont_id(c_cord, [-1, -6, -7], c_cords, for_dead))
                continue
            line_1 = ['b1', 'c1', 'd1', 'e1']
            step_1 = [6, 1, -1, 5, 7]
            if c_cord in line_1:  # если клетка корабля на верхней горизонтальной линии
                d.update(self.cont_id(c_cord, step_1, c_cords, for_dead))
                continue
            line_6 = ['b6', 'c6', 'd6', 'e6']
            step_6 = [-1, 1, -6, -5, -7]
            if c_cord in line_6:  # если клетка корабля на нижней горизонтальной линии
                d.update(self.cont_id(c_cord, step_6, c_cords, for_dead))
                continue

            line_a = ['a2', 'a3', 'a4', 'a5']
            step_a = [1, 6, -6, -5, 7]
            if c_cord in line_a:  # если клетка корабля на левой вертикальной линии
                d.update(self.cont_id(c_cord, step_a, c_cords, for_dead))
                continue

            line_f = ['f2', 'f3', 'f4', 'f5']
            step_f = [-1, 6, -6, 5, -7]
            if c_cord in line_f:  # если клетка корабля на правой боковой линии
                d.update(self.cont_id(c_cord, step_f, c_cords, for_dead))
                continue

            steps = [-7, -6, -5, -1, +1, +5, +6, +7]
            if c_cord:  # если клетка корабля не на краю
                d.update(self.cont_id(c_cord, steps, c_cords, for_dead))
        return d

    def shot(self, shooter, xy, dots):  # требует стреляющего, координата выстрела и экземпляр класса Dots
        """Требует str(стреляющего), str(координата выстрела) и экземпляр класса Dots.
            Возвращает 0 - мимо, 'same' - в эту клетку уже был сделан выстрел
            1 - ранение, 2 - уничтожил.
        """

        if shooter == 'pl':
            if xy in self.keys:
                if self._b_ai[xy] == '◦':
                    self._b_ai[xy] = '◌'
                    return 0  # мимо
                elif self._b_ai[xy] == ' ':
                    self._b_ai[xy] = '◌'
                    return 0
                elif self._b_ai[xy] in ['◙', '◌', '■']:
                    return 'same'

                elif self._b_ai[xy] == '□':
                    damage = dots.damage(shooter, xy)  # изменение модели корабля и возвращать колл жизней данного экземпляра

                    if 0 < damage[0] <= 3:
                        self._b_ai.update(damage[1])
                        return 1  # значит ранен
                    elif damage[0] == 0:
                        self._b_ai.update(damage[1])
                        contur = self.contour(damage[1], True)
                        self._b_ai.update(contur)
                        return 2  # Значит убит
                    elif 3 < damage[0] < 0:
                        raise BattleShipExc(f'Неправильно сработал метод подсчета жизней= {damage[0]}')
            else:
                raise BattleShipExc("Неправильные координаты Выстрела!")
        else:
            if xy in self.keys:
                if self._b_p[xy] == '◦':
                    self._b_p[xy] = '◌'
                    return 0
                elif self._b_p[xy] == ' ':
                    self._b_p[xy] = '◌'
                    return 0
                elif self._b_p[xy] in ['◙', '◌', '■']:
                    return 'same'
                elif self._b_p[xy] == '□':
                    damage = dots.damage(shooter, xy)  # изменение модели корабля и возвращать колл жизней
                    # pl_ship_m3 = damage[2]
                    if 0 < damage[0] <= 3:
                        self._b_p.update(damage[1])
                        return 1
                        # if pl_ship_m3:
                        #     return pl_ship_m3
                        # else:
                        #     return 1
                    elif damage[0] == 0:
                        self._b_p.update(damage[1])
                        contur = self.contour(damage[1], True)
                        self._b_p.update(contur)
                        return 2
                    elif 3 < damage[0] < 0:
                        raise BattleShipExc(f'Неправильно сработал метод подсчета жизней= {damage[0]}')
            else:
                raise BattleShipExc(f"Неправильные координаты Выстрела! self, shooter={shooter}, xy={xy},")

    def virt_board(self):
        targets_d = {}  #
        for_random_shot = []  # список для рандомного выстрела ИИ

        for cord, cell in self._b_p.items():

            if cell == '◦' or cell == ' ' or cell == '□':
                cell = 1
                for_random_shot.append(cord)
            else:
                cell = 0
            targets_d[cord] = cell

        return [targets_d, for_random_shot]
