import numpy as np

class MathModule:
    def __init__(self, x0, y0, v0, angleDeg, fps, g, dt = 0.01):
        self.x0 = x0  # початкова координата x
        self.y0 = y0  # початкова координата y
        self.v0 = v0  # швидкість
        self.angleRad = np.radians(angleDeg)     # кут
        self.dt = 0.01                           # крок (хардкод тому що немає сенсу задавати руками)
        self.g = g                               # Прискорення вільного падіння

    def DoCalculations(self):
        # Розклад (карт таро) векторів швидкості на проекції X/Y
        v0x = self.v0 * np.cos(self.angleRad)
        v0y = self.v0 * np.sin(self.angleRad)

        # Обмеження часу (на випадок, якщо об'єкт буде летіти 3 роки)
        tMax = 1000

        # Генерація масиву часу
        # від 0 до tMax з кроком dt
        tFull = np.arange(0, tMax, self.dt)

        # Генерація масиву координат (по часу)
        xFull = self.x0 + v0x * tFull
        yFull = self.y0 + v0y * tFull - (self.g * tFull ** 2) / 2

        # Знаходження індексів, де y >= 0
        validIndices = np.where(yFull >= 0)[0]

        # Якщо тіло відразу під землею - повертається початкова точка
        # UPD: можливо, вже лишнє (добавлені перевірки)
        if len(validIndices) == 0:
            return np.array([self.x0]), np.array([self.y0]), 0.0, self.x0

        # Обрізка масивів по останній валідній точці
        lastIndex = validIndices[-1]
        x = xFull[:lastIndex + 1]
        y = yFull[:lastIndex + 1]

        # Примусово даємо останній точці y координату 0
        y[-1] = 0.0

        # Обчислення часу
        totalTime = len(x) * self.dt

        # Обчислення дальності
        distance = x[-1] - self.x0

        # масиви координат x, y, загальний час, дистанція
        return x, y, totalTime, distance


if __name__ == "__main__":
    model = MathModule(
        x0 = 5,
        y0 = 0,
        v0 = 10,
        angleDeg = 45,
        fps = 30,
        g = 9.81,
    )

    x, y, totalTime, distance = model.DoCalculations()

    print(
        "\ninfo block btw\n\n"
        f"\tЗгенеровано точок: {len(x)}\n" +
        f"\tОстання точка X: {x[-1]}\n" +
        f"\tОстання точка Y: {y[-1]}\n" +
        f"\tЧас польоту: {totalTime}\n" +
        f"\tВідстань: {distance}\n"
    )
