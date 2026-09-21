from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a: int, b: int):
        pass

    @abstractmethod
    def symbol(self) -> str:
        pass


class Addition(Operation):
    def execute(self, a: int, b: int) -> int:
        return a + b

    def symbol(self) -> str:
        return "+"


class Multiplication(Operation):
    def execute(self, a: int, b: int) -> int:
        return a * b

    def symbol(self) -> str:
        return "*"


class Division(Operation):
    def execute(self, a: int, b: int) -> float:
        if b == 0:
            raise ValueError("Ошибка: деление на ноль!")
        return a / b

    def symbol(self) -> str:
        return "/"


class Subtraction(Operation):
    def execute(self, a: int, b: int) -> int:
        return a - b

    def symbol(self) -> str:
        return "-"


class Power(Operation):
    def execute(self, a: int, b: int) -> int:
        return a ** b

    def symbol(self) -> str:
        return "^"


class Factorial(Operation):
    def execute(self, a: int, b: int = 0) -> int:
        if a < 0:
            raise ValueError("Ошибка: факториал отрицательного числа не существует!")
        if a == 0 or a == 1:
            return 1
        return a * self.execute(a - 1)

    def symbol(self) -> str:
        return "!"


class Calculator:
    def __init__(self):
        self.operations = {
            "1": Addition(),
            "2": Multiplication(),
            "3": Division(),
            "4": Subtraction(),
            "5": Power(),
            "6": Factorial()
        }

    def show_menu(self):
        print("Доступные операции:")
        print("1 - Сложение")
        print("2 - Умножение")
        print("3 - Деление")
        print("4 - Вычитание")
        print("5 - Возведение в степень")
        print("6 - Факториал")
        print("0 - Выход")

    def calculate(self, choice: str, a: int, b: int = 0) -> bool:
        if choice == "0":
            print("До свидания!")
            return False

        operation = self.operations.get(choice)

        if operation is None:
            print("Неверный выбор! Попробуйте снова.")
            return True

        try:
            result = operation.execute(a, b)

            if choice == "6":
                print(f"{a}{operation.symbol()} = {result}")
            else:
                print(f"{a} {operation.symbol()} {b} = {result}")

        except ValueError as error:
            print(error)

        return True

    def run(self):
        self.show_menu()
        running = True

        while running:
            print("\n" + "-" * 30)
            choice = input("Выберите операцию (0-6): ")

            if choice == "0":
                running = self.calculate(choice, 0, 0)
                continue

            try:
                a = int(input("Введите первое число: "))

                if choice != "6":
                    b = int(input("Введите второе число: "))
                else:
                    b = 0

            except ValueError:
                print("Ошибка: введите целые числа!")
                continue

            running = self.calculate(choice, a, b)


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()