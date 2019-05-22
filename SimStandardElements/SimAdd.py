from PySimCore import SimBaseClass, sim_property, paint_func, SimPainter


# Данный компонент может складывать и вычитать значения.
# Поведение будет определяться строковой переменной signs.
# Если i-й символ строки будет равен "+" то значение будет прибавляться,
# а если "-" то вычитаться.
class SimAdd(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        self.inputs = []  # список входных сокетов. Данный список используется в функции update,
        # поэтому он должен быть создан но вызова конструктора предка
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()  # единственный выходной сокет
        self.set_sockets_to_positions()  # функция, которая ставит сокеты на свои места

    def update(self, new_properties: dict):
        if 'signs' not in new_properties:  # значение по умолчанию
            self.signs = '++'
        else:
            self.signs = ''
            for sign in new_properties['signs']:
                if sign in ['-', '+']:  # добавляем знаки
                    self.signs += sign

        for i in range(len(self.signs) - len(self.inputs)):  # создаем сокеты, если их меньше, чем знаков
            self.inputs.append(self.new_input_socket())
        for i in range(len(self.inputs) - len(self.signs)):  # удаляем сокеты, если их больше, чем знаков
            self.delete_socket(self.inputs.pop())

    @sim_property
    def signs(self):  # signs - это свойство, обращение к ней как к обычной переменной,
        pass          # при этом значение будет сохраняться

    @staticmethod
    def get_name() -> str:  # имя компонента
        return 'Add'

    def init_simulation(self, context):
        pass  # никаких действий не неужно

    def iterate(self, time: float, context):
        total_sum = 0  # итоговая сумма
        for i, socket in enumerate(self.inputs):
            if self.signs[i] == '+':
                total_sum += socket.get_value()  # получение значения из сокета
            elif self.signs[i] == '-':
                total_sum -= socket.get_value()

        self.output.put_value(total_sum)  # в выходной сокет кладется итоговая сумма

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        # общее рисование
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.set_pen_width(3)
        painter.draw_line(x + w / 2, y + h / 5, x + w / 2, y + h * 4 / 5)
        painter.draw_line(x + w / 5, y + h / 2, x + w * 4 / 5, y + h / 2)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        # рисование конкретного компонента
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        for i, sign in enumerate(self.signs):
            painter.draw_text(x + self.inputs[i].x_in_parent + 14,
                              y + self.inputs[i].y_in_parent + 10, sign, self.font)
