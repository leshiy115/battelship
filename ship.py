
from board import BattleShipExc

class Ship:
    def __init__(self, b, m, xy, pos=None):
        # нос всегда самая верхняя или самая левая часть
        # pos или == 'g'(горизонтальная) или == v (вертикальная)
        self.board = b
        self.m = m
        self.xy = xy
        self.pos = pos
        self.body = self.body_loc()

    def body_loc(self):  # единожды создает тело при инициализации
        """Создаем словарь, где ключ: координаты части тела,
        значение: символ тела(зависящий от того подбит ли он или нет)
        Если тело корабля выходит за рамки карты выдает исключение"""
        body_d = {}
        if self.pos == 'v':  # при горизонтальном положении: к цифровой координате добавляем 1.
            for x in range(self.m):
                xy = f"{self.xy[0]}{int(self.xy[1]) + 1*x}"
                if xy not in self.board.keys:
                    raise BattleShipExc(f'xy={self.xy}, m={self.m}, pos={self.pos} Корабль выходит за рамки карты')
                else:
                    body_d[xy] = '□'
            return body_d

        if self.pos == 'g':  # при вертикальном меняется буквенная координата. следующую букву находим методами chr() и ord() из таблицы символов Unicode
            for x in range(self.m):
                xy = f"{chr(ord(self.xy[0]) + x)}{self.xy[1]}"
                if xy not in self.board.keys:
                    raise BattleShipExc(f'xy={self.xy}, m={self.m}, pos={self.pos} Корабль выходит за рамки карты')
                else:
                    body_d[xy] = '□'
            return body_d

        if self.pos is None:  # если корабль одноклеточный)).
            if self.xy not in self.board.keys:
                raise BattleShipExc(f'xy={self.xy}, m={self.m}, pos={self.pos} Корабль выходит за рамки карты')
            else:
                body_d = {f"{self.xy}": '□'}
            return body_d

    def rest_life(self):
        if list(self.body.values()).count('■') == self.m:
            return 0
        else:
            return self.m - list(self.body.values()).count('◙')
