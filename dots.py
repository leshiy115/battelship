
from board import BattleShipExc


class Dots:
    def __init__(self, f_p, f_ai):
        self.f_p = f_p
        self.f_ai = f_ai
        self.all_d = self.all_ships_p()

    def all_ships_p(self):
        """ Из предоставленных классу списков ссылок на все созданные корабли создает 3 словаря для работы методов.
        пример: через self.all_d[0]['pl']['b4'] получаем из флота игрока объект модели ship, чье тело там расположено."""
        fleets_dict = {}
        ships_pl = {}
        ships_ai = {}
        for x in range(2):
            if x == 0:
                owner = 'ai'
                fleet = self.f_p
            else:
                owner = 'pl'
                fleet = self.f_ai
            d = {}

            for typ in fleet:
                tic = 1
                for ship in typ:
                    if owner == "ai":
                        if ship.m == 3:
                            ships_pl[f"M{ship.m}"] = ship
                        elif ship.m == 2:
                            ships_pl[f"M{ship.m}[{tic}]"] = ship
                            tic += 1
                        else:
                            ships_pl[f"M{ship.m}[{tic}]"] = ship
                            tic += 1
                    else:
                        if ship.m == 3:
                            ships_ai[f"M{ship.m}"] = ship
                        elif ship.m == 2:
                            ships_ai[f"M{ship.m}[{tic}]"] = ship
                            tic += 1
                        else:
                            ships_ai[f"M{ship.m}[{tic}]"] = ship
                            tic += 1
                    for cord in ship.body.keys():
                        d[cord] = ship

            fleets_dict[owner] = d

        return [fleets_dict, ships_pl, ships_ai]

    def damage(self, shooter, xy):
        """требует str(кто) стреляет и str(координаты)
        возвращает список из int-числа жизней, dict-тела корабля и информацию о попадании"""
        try:
            ship = self.all_d[0][shooter][xy]
            ship.body[xy] = '◙'
            life = ship.rest_life()
            if life == 0:
                for k in ship.body.keys():
                    ship.body[k] = '■'
            return [life, ship.body]

        except KeyError:
            raise BattleShipExc(f"""
            Выстрел не попал в корабль хотя на карте по
            падание было.\n
            def damage({shooter}, {xy}):\n
            self.all_d[0][{shooter}] = {self.all_d[0][shooter]}\n
            """)

    def fleet_left(self, owner):
        """Создает список из текстовых изображений кораблей.
        Удаляет из него потопленные.
        если возвращает None значит затребованный флот уничтожен"""
        if owner == "pl":
            del_lst = []  # список потопленных
            for k, ship in self.all_d[1].items():
                if ship.rest_life() == 0:
                    del_lst.append(k)
            for k in del_lst:  #
                self.all_d[1].pop(k)
            ships = []
            if self.all_d[1].values():
                for ship in self.all_d[1].values():
                    t = "".join([x for x in ship.body.values()])
                    ships.append(t)
            else:
                return None
            return ships

        elif owner == "ai":
            del_lst = []
            for k, ship in self.all_d[2].items():
                if ship.rest_life() == 0:
                    del_lst.append(k)
            for k in del_lst:
                self.all_d[2].pop(k)
            ships = []
            if self.all_d[2].values():
                for ship in self.all_d[2].values():
                    t = "".join([x for x in ship.body.values()])
                    ships.append(t)
            else:
                return None
            return ships
        else:
            raise BattleShipExc(f'Не передалась информация о владельце флота owner={owner}')
