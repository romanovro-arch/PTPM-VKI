def summ(a: int, b: int) -> int:
    return a + b


def umnoj(a: int, b: int) -> int:
    return a * b


def delenie(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Ошибка: деление на ноль!")
    return a / b


def minus(a: int, b: int) -> int:
    return a - b


def stepen(a: int, b: int) -> int:
    return a ** b


def chooser(d: str, a: int, b: int):
    match d:
        case '0':
            print("До свидания!")
            return False
        case '1':
            result = summ(a, b)
            print(f"{a} + {b} = {result}")
            return True
        case '2':
            result = umnoj(a, b)
            print(f"{a} * {b} = {result}")
            return True
        case '3':
            result = delenie(a, b)
            if isinstance(result, str):
                print(result)
            else:
                print(f"{a} / {b} = {result}")
            return True
        case '4':
            result = minus(a, b)
            print(f"{a} - {b} = {result}")
            return True
        case '5':
            result = stepen(a, b)
            print(f"{a} ^ {b} = {result}")
            return True
        case _:
            print("Неверный выбор! Попробуйте снова.")
            return True


def calc():
    print("Доступные операции:")
    print("1 - Сложение")
    print("2 - Умножение")
    print("3 - Деление")
    print("4 - Вычитание")
    print("5 - Возведение в степень")
    print("0 - Выход")

    running = True
    while running:
        print("\n" + "-" * 30)
        choice = input("Выберите операцию (0-5): ")

        if choice == '0':
            running = chooser(choice, 0, 0)
            continue

        try:
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
        except ValueError:
            print("Ошибка: введите целые числа!")
            continue

        running = chooser(choice, a, b)


if __name__ == "__main__":
    calc()