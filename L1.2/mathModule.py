import numpy as np

class MathModule:
    def __init__(self, x0, y0, v0, a, angleDeg, totalTime, dt = 0.01):
        self.x0 = x0  # початкова координата x
        self.y0 = y0  # початкова координата y
        self.v0 = v0  # швидкість
        self.a = a    # прискорення
        self.angleRad = np.radians(angleDeg)   # кут
        self.totalTime = totalTime             # час проведення "експерименту"
        self.dt = dt                           # крок

    def DoCalculations(self):
        # Розклад (карт таро) векторів швидкості на проекції X/Y
        v0x = self.v0 * np.cos(self.angleRad)
        v0y = self.v0 * np.sin(self.angleRad)

        # Розклад векторів прискорення на проекції X/Y
        ax = self.a * np.cos(self.angleRad)
        ay = self.a * np.sin(self.angleRad)

        # Генерація масиву часу
        # від 0 до totalTime з кроком dt
        t = np.arange(0, self.totalTime + self.dt, self.dt)

        # Підстановка у рівняння (без циклів, дада от це і називається "оптимізація")
        x = self.x0 + v0x * t + (ax * t ** 2) / 2
        y = self.y0 + v0y * t + (ay * t ** 2) / 2

        # час, масиви координат x та y
        return t, x, y


if __name__ == "__main__":
    model = MathModule(
        x0 = 0,
        y0 = 0,
        v0 = 10,
        a = 2,
        angleDeg = 45,
        totalTime = 5
    )

    t, x, y = model.DoCalculations()

    print(
        "\ninfo block btw\n\n"
        f"\tЗгенеровано точок: {len(t)}\n" +
        f"\tОстання точка X: {x[-1]}\n" +
        f"\tОстання точка Y: {y[-1]}"
    )
