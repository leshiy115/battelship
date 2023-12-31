import sys
import os  # для os.system('cls')
from board import Board
from board import BattleShipExc
from ship import Ship
from dots import Dots
import random
import time



class Ai:

    """ ИИ. Требует экземпляр доски и уровень сложности.
    на низком уровне сложности стреляет случайно по свободным клеткам. При попадании создает список следующих возможных позиций."""

    def __init__(self, board, dif=1):
        self.b = board
        self.dif = dif
        self.hit_count = 0
        self.next_pos_hit = []
        self.m3 = True
        self.m3_body = []
        self.m2_count = 2
        self.rand = self.diagonal_shooting() if random.randint(1, 2) == 1 else self.diagonal_shooting_r()  # сначала создал одну функцию для выбора стрельбы по диагоналям или реверс диагоналям. она выбирала и возвращала 1 из вариантов. но почему-то иногда их перемешивала. получались гибридные списки. для м3 нормальные диагонали для м2 берется реверс. так и не понял почему.
        self.find_m3 = self.rand[0]
        self.find_m2 = self.rand[1]
        self.v_board = self.b.virt_board()[1]


    def diagonal_shooting(self):
        """Создает список координат для стрельбы по диагоналям.
        Ускоряет поиск м3 и м2 кораблей"""
        diags_m3 = [self.b.keys[3:18:7], self.b.keys[::7], self.b.keys[18::7]]
        find_m3 = []
        for x in diags_m3:
            find_m3.extend(x)
        m2_diags = [['f1'], self.b.keys[2:24:7], self.b.keys[::7],
                    self.b.keys[12::7], ['a5']]
        find_m2 = []
        for x in m2_diags:
            find_m2.extend(x)
        return [find_m3, find_m2]

    # def diagonal_shooting(self):  # проблемный код перемешивающий то что не должен.
    #     """Создает список координат для стрельбы по диагоналям.
    #     diags_m3 = self.b.keys[3:18:7], self.b.keys[::7], self.b.keys[18::7]
    #     find_m3 = []
    #     for x in diags_m3:
    #         find_m3.extend(x)
    #     diags_m3_r = self.b.keys[2:13:5], self.b.keys[5:31:5], self.b.keys[23::5]
    #     find_m3_r = []
    #     for x in diags_m3_r:
    #         find_m3_r.extend(x)
    #     m2_diags = self.b.keys[4:12:7], self.b.keys[2:24:7], self.b.keys[::7], self.b.keys[12::7], self.b.keys[24::7]
    #     m2_find = []
    #     for x in m2_diags:
    #         m2_find.extend(x)
    #     diags_m2_r = self.b.keys[1:7:5], self.b.keys[3:19:5], self.b.keys[5:31:5], self.b.keys[17::5], self.b.keys[29::5]
    #     m2_find_r = []
    #     for x in diags_m2_r:
    #         m2_find_r.extend(x)
    #     rand = [find_m3, m2_find]
    #     rand_r = [find_m3_r, m2_find_r]
    #     r = random.randint(0, 1)
    #     ret = rand if r == 0 else rand_r
    #     return ret

    def diagonal_shooting_r(self):
        diags_m3_r = [self.b.keys[2:13:5], self.b.keys[5:31:5], self.b.keys[23::5]]
        find_m3_r = []
        for x in diags_m3_r:
            find_m3_r.extend(x)
        diags_m2_r = [['a1'], self.b.keys[3:19:5], self.b.keys[5:31:5],
                      self.b.keys[17::5], ['f6']]
        find_m2_r = []
        for x in diags_m2_r:
            find_m2_r.extend(x)
        return [find_m3_r, find_m2_r]

    def aiming_shot(self):
        pos_rand = random.choice(self.next_pos_hit)
        self.next_pos_hit.remove(pos_rand)
        if pos_rand in self.find_m3:
            self.find_m3.remove(pos_rand)
        if pos_rand in self.find_m2:
            self.find_m2.remove(pos_rand)
        return pos_rand  # сам выстрел возвращается

    def random_shot(self):
        self.v_board = self.b.virt_board()[1]
        for crds in self.find_m3:
            if crds not in self.v_board:
                self.find_m3.remove(crds)
        for crds in self.find_m2:
            if crds not in self.v_board:
                self.find_m2.remove(crds)

        if self.dif == 1:
            crd = random.choice(self.v_board)
            return crd
        else:
            if self.m3:
                pos_rand = self.find_m3.pop()
                return pos_rand
            if self.m2_count > 0 and not self.m3:
                if len(self.find_m2) > 0:
                    pos_rand = self.find_m2.pop()
                    if pos_rand not in self.v_board:
                        crd = random.choice(self.v_board)
                        return crd
                else:
                    return random.choice(self.v_board)

                return pos_rand
            else:  # остались м1
                crd = random.choice(self.v_board)
                return crd

    def if_hit(self, last_shot):
        self.v_board = self.b.virt_board()[1]
        lst = []
        next_shot = []
        if last_shot[0] == 'a':
            lst.append(1)
        elif last_shot[0] == 'f':
            lst.append(-1)
        else:
            lst.append(1)
            lst.append(-1)

        if last_shot[1] == '1':
            lst.append(6)
        elif last_shot[1] == '6':
            lst.append(-6)
        else:
            lst.append(6)
            lst.append(-6)

        for step in lst:
            last_shot_id = self.b.keys.index(last_shot)
            pos_shot_id = last_shot_id + step
            if pos_shot_id < 0:
                continue
            pos_shot_cords = self.b.keys[pos_shot_id]

            if pos_shot_cords in self.v_board:
                next_shot.append(pos_shot_cords)
            else:
                continue
        if len(next_shot) == 0:
            raise BattleShipExc(f"ИИ проверил все возможные варианты выстрела и не выбрал"
                                f"self.b.virt_board()[1] = {self.v_board}\n lst for next step={lst}/n"
                                f"last_shot= {last_shot}")
        return next_shot


    def tern(self, last_shot=None, last_shot_info=None):
        """Требует информацию о последнем выстреле.
        str(last_shot) - координаты выстрела
        int(last_shot_info) - информация попал или нет"""
        self.v_board = self.b.virt_board()[1]

        if last_shot_info == 2:
            self.hit_count = 0
            self.m3_body = []
            self.next_pos_hit = []
            for crds in self.find_m3:
                if crds not in self.v_board:
                    self.find_m3.remove(crds)
            for crds in self.find_m2:
                if crds not in self.v_board:
                    self.find_m2.remove(crds)


            return self.random_shot()

        if not last_shot:  # я еще не стрелял
            return self.random_shot()

        if last_shot_info == 0 and self.hit_count == 0:  # я стрелял, но мимо
            return self.random_shot()

        if last_shot_info == 1 and self.hit_count == 0:  # я наконец попал ! создаем список!! вариантов следующего выстрела! пока не убью не забуду.
            self.hit_count += 1
            self.m2_count -= 1
            self.m3_body.append(last_shot)
            self.next_pos_hit = self.if_hit(last_shot)  # метод создает список возможных координат для выстрела и сохраняет в классе.
            return self.aiming_shot()  # сам выстрел возвращается

        if last_shot_info == 0 and self.hit_count == 1:  # я попадал до этого. еще раз из списка!
            return self.aiming_shot()

        if last_shot_info == 1 and self.hit_count == 1:  # Это м3! Потому что у меня было попадание до этого!
            self.v_board = self.b.virt_board()[1]
            self.hit_count += 1
            self.m2_count += 1
            self.m3 = False
            self.m3_body.append(last_shot)
            self.next_pos_hit = []
            cord_1 = self.m3_body[0]
            cord_2 = self.m3_body[1]
            if cord_1[0] == cord_2[0]:
                n_cord_1 = int(cord_1[1])
                n_cord_2 = int(cord_2[1])
                pos_n_1 = n_cord_1 + 1 if n_cord_1 > n_cord_2 else n_cord_2 + 1
                pos_n_2 = n_cord_1 - 1 if n_cord_1 < n_cord_2 else n_cord_2 - 1
                if 0 < pos_n_1 < 7:
                    cord_pos_1 = cord_1[0] + str(pos_n_1)
                    if cord_pos_1 in self.v_board:
                        self.next_pos_hit.append(cord_pos_1)
                if 0 < pos_n_2 < 7:
                    cord_pos_2 = cord_1[0] + str(pos_n_2)
                    if cord_pos_2 in self.v_board:
                        self.next_pos_hit.append(cord_pos_2)
            elif cord_1[1] == cord_2[1]:
                l_cord_1 = cord_1[0]
                l_cord_2 = cord_2[0]
                pos_l_1 = chr(ord(l_cord_1) + 1) if l_cord_1 > l_cord_2 else chr(ord(l_cord_2) + 1)
                pos_l_2 = chr(ord(l_cord_1) - 1) if l_cord_1 < l_cord_2 else chr(ord(l_cord_2) - 1)
                l_cords = ['a', 'b', 'c', 'd', 'e', 'f']
                if pos_l_1 in l_cords:
                    cord_pos_1 = pos_l_1 + cord_1[1]
                    if cord_pos_1 in self.v_board:
                        self.next_pos_hit.append(cord_pos_1)
                if pos_l_2 in l_cords:
                    cord_pos_2 = pos_l_2 + cord_1[1]
                    if cord_pos_2 in self.v_board:
                        self.next_pos_hit.append(cord_pos_2)
            else:
                raise BattleShipExc(f'вроде это м3 но позиция не определяется self.m3_body={self.m3_body}')


            if len(self.next_pos_hit) == 0:
                raise BattleShipExc(f'ИИ должен был создать максимум 2 варианта след выстрелов!'
                                    f'self.next_pos_hit={self.next_pos_hit}, '
                                    f'self.m3_body={self.m3_body}, self.b.virt_board()[1]={self.v_board}')
            return self.aiming_shot()

        if last_shot_info == 0 and self.hit_count == 2:  # это точно м3! теперь я знаю куда стрелять
            self.m3 = False
            return self.aiming_shot()

        if last_shot_info == 1 and self.hit_count == 2:  # это точно м3! теперь я знаю куда стрелять
            self.m3 = False
            return self.aiming_shot()

        if last_shot_info not in [0, 1, 2] or self.hit_count > 2:
            raise BattleShipExc(f'ИИ стрелял по той же клетке или неправильно считал попадания'
            f'last_shot_info={last_shot_info}\n last_shot={last_shot} \nself.hit_count={self.hit_count}\n'
                                f'self.v_board= {self.v_board}\n'
                                f'self.find_m2= {self.find_m2}\n'
                                f'self.find_m3= {self.find_m3}\n'
                                f'self.b.b_p={self.b.b_p}\n'
                                f'self.m3_body = {self.m3_body}')


class Game:
    """
    Для игры через консоль в Pycharm желательно включить эмуляцию python консоли. Сделать это можно на панели Run в настройках кликнув на значок ключа под значком треугольника 'play'. Затем в Execution поставить галочку напротив "Emulate terminal in output console". В эти настройки также можно попасть через зажатие (Shift Alt F10).
    Или найдите соответсвующую настройку в среде которую вы используете.
    Без выполнения этих шагов экран консоли не будет очищаться от текста прошлого цикла.
    """
    def __init__(self):
        self.b = Board()  #
        self.dif = 1
        self.ai = None
        self.d = None
        self.ai_win = 0
        self.pl_win = 0
        self.state = '\nСостояние флота ИИ -- | □□□ | □□ | □□ | □ | □ | □ | □ |'

        # self.auto_pl = None  # для автоигры

    def rand_fleet(self, k=9):  # Возвращает словарь флота
        """
        Генератор случайного расположения флота
        pl == 'pl' если игрок и "ai" если ИИ
        """
        rand_board = self.b.b_p.copy()  # виртуальный словарь. удаляем использованные ключи
        rand_fleet = {}
        pos = random.choice(['g', 'v'])  # создает рандомный □□□ с контуром.
        ship_m_3 = []

        if pos == "v":
            r_c = random.choice([x for x in rand_board if x[1] not in ['5', '6']])  # исключаем две нижних линии для достаточного места. потому что тело корабля рассчитывается от головы.
            ship = Ship(self.b, 3, r_c, pos)
            ship_m_3.append(ship)
            s_body = ship.body
            rand_fleet.update(s_body)
            [rand_board.pop(k) for k in s_body if k in rand_board]
            contur_dict = self.b.contour(s_body)
            for contur_c, cell in contur_dict.items():
                if rand_board.get(contur_c):
                    rand_board.pop(contur_c)
                    rand_fleet.update(dict([[contur_c, cell]]))
                continue
        else:
            r_c = random.choice([x for x in rand_board if x[0] not in ['e', 'f']])
            rand_board.pop(r_c)
            ship = Ship(self.b, 3, r_c, pos)
            ship_m_3.append(ship)
            s_body = ship.body
            rand_fleet.update(s_body)
            [rand_board.pop(k) for k in s_body if k in rand_board]
            contur_dict = self.b.contour(s_body)
            for contur_c, cell in contur_dict.items():
                if rand_board.get(contur_c):
                    rand_board.pop(contur_c)
                    rand_fleet.update(dict([[contur_c, cell]]))
                continue

        flag = True

        tic_long = 0
        while flag:  # цикл работает пока не разместит □□ с контуром.
            tic_long += 1
            rand_board_c1 = rand_board.copy()
            rand_fleet_c1 = rand_fleet.copy()
            ships_m_2 = []
            for x in range(2):
                pos = random.choice(['g', 'v'])
                if pos == "v":
                    r_c = random.choice([x for x in rand_board_c1 if x[1] != '6'])
                    ship_m_2 = Ship(self.b, 2, r_c, pos)
                    ships_m_2.append(ship_m_2)
                    s_body = ship_m_2.body
                    if list(s_body.keys())[1] not in rand_board_c1:  # если одна из точек тела корабля уже занята
                        break
                    rand_fleet_c1.update(s_body)
                    [rand_board_c1.pop(k) for k in s_body if k in rand_board_c1]
                    contur_dict = self.b.contour(s_body)
                    for contur_c, cell in contur_dict.items():
                        if rand_board_c1.get(contur_c):
                            rand_board_c1.pop(contur_c)
                            rand_fleet_c1.update(dict([[contur_c, cell]]))
                else:
                    r_c = random.choice([x for x in rand_board_c1 if x[0] != 'f'])
                    ship_m_2 = Ship(self.b, 2, r_c, pos)
                    ships_m_2.append(ship_m_2)
                    s_body = ship_m_2.body
                    if list(s_body.keys())[1] not in rand_board_c1:  # если одна из точек тела корабля уже занята
                        break
                    rand_fleet_c1.update(s_body)
                    [rand_board_c1.pop(k) for k in s_body if k in rand_board_c1]
                    contur_dict = self.b.contour(s_body)
                    for contur_c, cell in contur_dict.items():
                        if rand_board_c1.get(contur_c):
                            rand_board_c1.pop(contur_c)
                            rand_fleet_c1.update(dict([[contur_c, cell]]))
            else:
                # k  # чем больше число тем сильнее 2-м корабли жмутся к стенке, но быстрее генерация. не больше 12! иначе бесконечный цикл.
                if len(rand_board_c1.keys()) == k and len(ships_m_2) == 2:  ###!!!!
                    tic = 0
                    while True:  # цикл работает пока не разместит □ с контуром.
                        tic_long += 1
                        ships_m_1 = []
                        rand_board_c2 = rand_board_c1.copy()
                        rand_fleet_c2 = rand_fleet_c1.copy()
                        for x in range(4):  # создаем 4 одноклеточных.
                            if len(list(rand_board_c2.keys())) < 1:
                                break
                            r_c = random.choice(list(rand_board_c2.keys()))
                            ship_m_1 = Ship(self.b, 1, r_c)
                            ships_m_1.append(ship_m_1)
                            s_body = ship_m_1.body
                            rand_fleet_c2.update(s_body)
                            rand_board_c2.pop(r_c)
                            contur_dict = self.b.contour(s_body)
                            for contur_c, cell in contur_dict.items():
                                if rand_board_c2.get(contur_c):
                                    rand_board_c2.pop(contur_c)
                                    rand_fleet_c2.update(dict([[contur_c, cell]]))
                        else:
                            if len(ships_m_1) == 4:
                                rand_fleet.update(rand_fleet_c2)
                                ships = [ship_m_3, ships_m_2, ships_m_1]
                                d_fleet = {"rand_fleet": rand_fleet, "ships": ships}
                                return d_fleet
                            else:
                                continue
                        if tic > 50:  # если прошло много циклов, а корабли не разместились заново генерим □□
                            break
                        tic += 1
                        continue
                else:
                    continue

    def greet(self):
        while True:
            print("\nДобро пожаловать в игру Морской Бой! (только для версии python 3.7 и выше!)\n"
                  "\nОбщие правила всем известны, но объясню нюансы данной версии игры:\n"
                  "- Размер поля 6х6 клеток.\n"
                  "- Флот может состоять из 1-го □□□, 2-х □□ и 4-х □.\n"
                  "- Положение флота генерируется случайно согласно общеизвестным правилам.\n"
                  "- Вы не можете видеть расположение флота ИИ если не задели или не потопили его корабль.\n"
                  "- '□' - целый корпус корабля. '◙' - подбитая часть корабля. '■' - потопленный корабль полностью закрашивается.\n"
                  "- '◦' - не обстрелянная клетка моря. '◌' - обстрелянная клетка моря.\n"
                  "- Перед началом игры происходит случайный выбор за кем первый ход.\n"
                  "- Для выстрела введите координаты в формате: 'a6' (Буквы вводятся латиницей).\n"
                  "\n- Для игры через консоль в Pycharm желательно включить эмуляцию python консоли. Сделать это можно на панели Run в настройках кликнув на значок ключа под значком треугольника 'play'. Затем в Execution поставить галочку напротив 'Emulate terminal in output console'. В эти настройки также можно попасть через зажатие (Shift Alt F10). Или найдите соответсвующую настройку в среде которую вы используете. Без выполнения этих шагов экран консоли не будет очищаться от текста прошлого цикла.\n")
            while True:
                choice = input("    \nГлавное меню    \nВыберите один из вариантов, путем ввода символа.\n"
                               "'1' == Игра на низкой сложности.\n"
                               "'2' == Игра на средней сложности.\n"
                               "'3' == Повторно показать правила.\n"
                               "'q' == Выход.\n"
                               "Введите ваш выбор:  ")
                if choice == '1':
                    print("Игра начинается! Для выхода обратно в меню в любой момент введите 'q")
                    os.system('cls')
                    self.b = Board()  # обновляем доску
                    self.dif = 1
                    self.loop()

                elif choice == '2':
                    print("Игра начинается! Для выхода обратно в меню в любой момент введите 'q")
                    os.system('cls')
                    self.b = Board()  # обновляем доску
                    self.dif = 2
                    self.loop()
                elif choice == '3':
                    break
                elif choice == 'q':
                    sys.exit()
                else:
                    print("Неправильный ввод!")

    def loop(self):
        # self.auto_pl = iter(self.b.keys)  # для автоигры
        self.ai = Ai(self.b, self.dif)
        if self.dif == 1:
            fleet_p = self.rand_fleet()
            fleet_ai = self.rand_fleet()
        else:  # увеличиваем вероятность более удачной расстановки кораблей для ИИ. Параметр не жесткий и сильно не влияет.
            fleet_p = self.rand_fleet(k=8)
            fleet_ai = self.rand_fleet(k=12)
        self.b.b_p.update(fleet_p["rand_fleet"])  # добавляет на поле игрока его флот.
        self.b.b_ai.update(fleet_ai["rand_fleet"])
        self.d = Dots(fleet_p['ships'], fleet_ai['ships'])  # инициализируем класс и даем ему информацию о флотах


        last_shot = None  # сохраняем предыдущий выстрел для ИИ
        last_shot_info = None  # информацию о результате выстрела
        self.b.show_board()
        rand_first_tern = random.randint(0, 1)
        flag = True
        print("\n\t\t\t    Первый ход выпал ИИ" if rand_first_tern == 1 else "\n\t\t\t    Первый ход выпал Вам")
        self.state = '\nСостояние флота ИИ -- | □□□ | □□ | □□ | □ | □ | □ | □ |'
        print(self.state)
        while flag:
            if rand_first_tern == 0:
                flag = self.pl_tern()
                if flag:
                    ai_tern = self.ai_tern(last_shot, last_shot_info)
                    flag = ai_tern['flag']
                    last_shot = ai_tern['last_shot']
                    last_shot_info = ai_tern['last_shot_info']
            else:
                ai_tern = self.ai_tern(last_shot, last_shot_info)
                flag = ai_tern['flag']
                last_shot = ai_tern['last_shot']
                last_shot_info = ai_tern['last_shot_info']
                if flag:
                    flag = self.pl_tern()
        return

    def pl_tern(self):
        flag = True
        while True:

            while True:
                pl_shot = input("Ваш ход: ").lower()
                if pl_shot == 'q':
                    flag = False
                    return flag

                if pl_shot not in self.b.keys:
                    print("Неправильные координаты!\n")
                    continue
                else:
                    break
            # pl_shot = next(self.auto_pl)  # для автоигры
            time.sleep(1.5)
            last_shot_info = self.b.shot('pl', pl_shot, self.d)
            self.b.show_board('pl', last_shot_info)
            print(f"\n\t\t\t   Игрок стреляет на {pl_shot}")
            state = self.d.fleet_left('ai')
            if state:
                self.state = '\nСостояние флота ИИ -- | ' + " | ". join(state) + ' |'
            print(self.state)
            if not state:
                print('\n\t\t\t     !!!!ВЫ ВЫИГРАЛИ!!!!\n')
                self.pl_win += 1
                flag = False
                break
            if last_shot_info == 0:
                break
            elif last_shot_info == 1:
                continue
            elif last_shot_info == 2:
                continue
            elif last_shot_info == "same":
                print("Эта клетка не нуждается в обстреле!!")
                continue

        return flag

    def ai_tern(self, last_shot, last_shot_info):
        flag = True
        time.sleep(2)
        while True:
            if last_shot_info in [1, 2]:
                time.sleep(3)
            ai_shot = self.ai.tern(last_shot, last_shot_info)
            last_shot_info = self.b.shot('ai', ai_shot, self.d)
            last_shot = ai_shot
            self.b.show_board('ai', last_shot_info)
            print(f"\n\t\t\t     ИИ стреляет на {ai_shot}")
            print(self.state)
            state = self.d.fleet_left('pl')
            if not state:
                print('\n\t\t\t    !!!!ПОБЕДИТЕЛЬ ИИ!!!!\n')
                self.ai_win += 1
                flag = False
                break
            if last_shot_info == 0:
                break
            elif last_shot_info == 1:
                continue
            elif last_shot_info == 2:
                continue
            else:
                raise BattleShipExc(f'state={state}')
        return {'flag': flag, "last_shot": last_shot, "last_shot_info": last_shot_info}



if __name__ == "__main__":
    g = Game()
    g.greet()












