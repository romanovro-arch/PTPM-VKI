# 🛡️ Руководство к защите практического задания: Срез знаний по юнит-тестам

## 📌 Паспорт работы
* **Тема:** «Срез знаний по юнит-тестам (класс Converter)»
* **Дисциплина:** Проектирование и тестирование программных модулей (ПТПМ)
* **Студент:** Романов Р. О.
* **Ветка Git:** `Lab4`

---

## 🚀 Команды для демонстрации преподавателю

### 1. Автоматический прогон всех 26 тестов (100% OK):
```powershell
python -m unittest discover -v
```
> Автоматически находит и выполняет все **26 юнит-тестов** класса `Converter` за 0.002 секунды со статусом `OK`.

### 2. Запуск файла тестов напрямую:
```powershell
python -m unittest tests/test_converter.py -v
```

### 3. Запуск демонстрационного скрипта:
```powershell
python main.py
```
> Выводит автоматический расчет контрольных значений из каждого диапазона и проверку перехвата `ValueError` при `x = 0.0`.

---

## 📐 Алгоритм работы метода `Converter.do(x: float) -> int`

Метод принимает вещественное число `float` (с точностью 1 знак после запятой) и возвращает целое число `int`:

| Интервал значений $x$ | Возвращаемое значение | Описание и логика | Граничные примеры |
| :--- | :---: | :--- | :--- |
| **$x \in [100.7; +\infty)$** | `1000` | Число больше или равно `100.7`. | `100.7` $\rightarrow$ `1000`<br>`100.8` $\rightarrow$ `1000`<br>`200.0` $\rightarrow$ `1000` |
| **$x \in (0; 100.7)$** | `int(x)` | Отбрасывание дробной части положительного числа. | `100.6` $\rightarrow$ `100`<br>`65.7` $\rightarrow$ `65`<br>`0.1` $\rightarrow$ `0` |
| **$x == 0.0$** | **`ValueError`** | Точка нуля (аналог `ArgumentException`). Генерируется исключение. | `0.0`, `-0.0`, `0` $\rightarrow$ `raises ValueError` |
| **$x \in [-30.4; 0)$** | `int(x) - 5` | Отбрасывание дробной части (`int(x)`) минус 5. | `-0.1` $\rightarrow$ `0 - 5 = -5`<br>`-1.5` $\rightarrow$ `-1 - 5 = -6`<br>`-30.4` $\rightarrow$ `-30 - 5 = -35` |
| **$x \in (-\infty; -30.5]$** | `-2000` | Число меньше или равно `-30.5`. | `-30.5` $\rightarrow$ `-2000`<br>`-30.6` $\rightarrow$ `-2000`<br>`-94.5` $\rightarrow$ `-2000` |

---

## 🧪 Структура 26 юнит-тестов (`tests/test_converter.py`)

1. **Диапазон $[100.7; +\infty)$ (3 теста):**
   - `test_upper_boundary_exact_point`: точная граница `100.7` $\rightarrow$ `1000`;
   - `test_upper_boundary_just_above`: точка `100.8` $\rightarrow$ `1000`;
   - `test_upper_boundary_large_numbers`: большие числа `200.0`, `1000.5`, `99999.9` $\rightarrow$ `1000`.

2. **Диапазон $(0; 100.7)$ (5 тестов):**
   - `test_positive_range_just_below_100_7`: точка `100.6` $\rightarrow$ `100`;
   - `test_positive_range_spec_example`: контрольный пример из ТЗ `65.7` $\rightarrow$ `65`;
   - `test_positive_range_integer_float`: число `50.0` $\rightarrow$ `50`;
   - `test_positive_range_small_values`: числа `1.9` $\rightarrow$ `1`, `1.0` $\rightarrow$ `1`;
   - `test_positive_range_near_zero`: нижняя граница `0.1` $\rightarrow$ `0`.

3. **Обработка нуля $x == 0.0$ (3 теста):**
   - `test_zero_raises_value_error`: `0.0` $\rightarrow$ проверка генерации `ValueError`;
   - `test_negative_zero_raises_value_error`: `-0.0` $\rightarrow$ `ValueError`;
   - `test_integer_zero_raises_value_error`: целое `0` $\rightarrow$ `ValueError`.

4. **Диапазон $[-30.4; 0)$ (5 тестов):**
   - `test_negative_range_near_zero`: точка `-0.1` $\rightarrow$ `int(-0.1) - 5 = -5`;
   - `test_negative_range_small_values`: точки `-1.5` $\rightarrow$ `-6`, `-1.0` $\rightarrow$ `-6`;
   - `test_negative_range_medium_values`: точки `-10.0` $\rightarrow$ `-15`, `-25.9` $\rightarrow$ `-30`;
   - `test_negative_range_just_before_boundary`: точка `-30.3` $\rightarrow$ `-35`;
   - `test_negative_range_exact_boundary`: точная граница `-30.4` $\rightarrow$ `-35`.

5. **Диапазон $(-\infty; -30.5]$ (4 теста):**
   - `test_lower_boundary_exact_point`: точная граница `-30.5` $\rightarrow$ `-2000`;
   - `test_lower_boundary_just_below`: точка `-30.6` $\rightarrow$ `-2000`;
   - `test_lower_boundary_spec_example`: пример из ТЗ `-94.5` $\rightarrow$ `-2000`;
   - `test_lower_boundary_large_negative_numbers`: большие отрицательные `-500.0`, `-99999.9` $\rightarrow$ `-2000`.

6. **Проверка типов входных данных (4 теста):**
   - `test_invalid_type_string_raises_type_error`: передача строки `'100.7'` $\rightarrow$ `TypeError`;
   - `test_invalid_type_none_raises_type_error`: передача `None` $\rightarrow$ `TypeError`;
   - `test_invalid_type_boolean_raises_type_error`: передача `True` $\rightarrow$ `TypeError`;
   - `test_invalid_type_list_raises_type_error`: передача списка `[10.5]` $\rightarrow$ `TypeError`.

7. **Проверка контракта метода (2 теста):**
   - `test_method_is_staticmethod`: проверка декоратора `@staticmethod`;
   - `test_call_via_instance`: возможность вызова через экземпляр `Converter().do(...)`.

---

## 💣 Ответы на вопросы преподавателя к защите

### Вопрос 1: *«Почему метод do сделан статическим (@staticmethod)?»*
> **Ответ:**  
> «В п. 1 технического задания дана жесткая сигнатура:  
> ```python
> @staticmethod
> def do(x: float) -> int:
> ```
> Статический метод не зависит от состояния экземпляра (`self`), работает как чистая математическая функция и может вызываться напрямую через класс: `Converter.do(100.7)`.»

---

### Вопрос 2: *«Как в Python работает int(x) для отрицательных чисел в диапазоне [-30.4; 0)?»*
> **Ответ:**  
> «Функция `int(x)` в Python выполняет усечение (truncation) в сторону нуля, просто отбрасывая дробную часть.  
> Например:  
> - `int(-0.1) == 0` $\rightarrow$ результат: `0 - 5 = -5`.  
> - `int(-1.5) == -1` $\rightarrow$ результат: `-1 - 5 = -6`.  
> - `int(-30.4) == -30` $\rightarrow$ результат: `-30 - 5 = -35`.  
> Это строго соответствует формулировке задания: *«целую часть числа x путем отбрасывания дробной части (эквивалентно int(x)) минус 5»*.»

---

### Вопрос 3: *«Какие техники тест-дизайна вы применили?»*
> **Ответ:**  
> 1. **Эквивалентное разбиение (Equivalence Partitioning):** входные данные разбиты на 5 взаимоисключающих классов: $[100.7; +\infty)$, $(0; 100.7)$, точка $\{0.0\}$, $[-30.4; 0)$ и $(-\infty; -30.5]$.
> 2. **Анализ граничных значений (Boundary Value Analysis):** протестированы все граничные точки и соседние с ними значения: $100.7$ и $100.6$; $0.1$ и $0.0$; $-0.1$ и $-30.4$; $-30.5$ и $-30.6$.
> 3. **Негативное тестирование (Negative Testing):** проверена реакция на недопустимые типы данных (`None`, строки, булевы значения) и исключение `ValueError` при нуле.

---

### Вопрос 4: *«Почему для float сделано округление round(float(x), 1)?»*
> **Ответ:**  
> «В стандарте IEEE 754 числа с плавающей точкой не могут быть абсолютно точно представлены в двоичном виде (например, `100.7` в памяти машины представляется как `100.69999999999999`). Округление `round(float(x), 1)` гарантирует соответствие заявленной в ТЗ точности в 1 знак после запятой и защищает от погрешностей машинной арифметики.»
