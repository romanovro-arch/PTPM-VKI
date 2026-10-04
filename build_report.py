import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def create_report():
    doc = Document()

    # Поля страницы: по 2 см (ок. 1134 dxa)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Настройка базового стиля текста
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # --- ТИТУЛЬНЫЙ БЛОК ---
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РФ\nНОВОСИБИРСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ\nВЫСШИЙ КОЛЛЕДЖ ИНФОРМАТИКИ (ВКИ НГУ)")
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title1 = p_title.add_run("ОТЧЕТ ПО ЛАБОРАТОРНОЙ РАБОТЕ №2\n")
    r_title1.font.size = Pt(16)
    r_title1.font.bold = True
    r_title1.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    r_title2 = p_title.add_run("Тема: «Юнит-тестирование проектов и автоматизация проверок»\n")
    r_title2.font.size = Pt(13)
    r_title2.font.bold = True

    r_title3 = p_title.add_run("Дисциплина: Проектирование и тестирование программных модулей (ПТПМ)")
    r_title3.font.size = Pt(11)
    r_title3.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(30)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_meta = p_meta.add_run(
        "Выполнил: студент Романов Р. О.\n"
        "Специальность: Информационные системы и программирование\n"
        "Проверил: Мастер практики\n"
        "Репозиторий: https://github.com/romanovro-arch/PTPM-VKI\n"
        "Ветка: Lab2"
    )
    r_meta.font.size = Pt(11)

    doc.add_paragraph().paragraph_format.space_after = Pt(40)

    p_city = doc.add_paragraph()
    p_city.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_city = p_city.add_run("Новосибирск, 2026")
    r_city.font.size = Pt(11)
    r_city.font.bold = True

    doc.add_page_break()

    # --- 1. ВВЕДЕНИЕ ---
    h1 = doc.add_heading("1. Цель и задачи работы", level=1)
    h1.style.font.name = 'Times New Roman'
    h1.style.font.size = Pt(14)
    h1.style.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    doc.add_paragraph(
        "Цель работы — освоение методологии модульного тестирования (Unit Testing) с использованием стандартного "
        "фреймворка unittest в Python, приобретение навыков декомпозиции требований, разработки тестовых сценариев "
        "для граничных и эквивалентных условий, а также выявление и локализация логических дефектов в предоставленном модуле."
    )
    doc.add_paragraph(
        "В ходе работы решены следующие задачи:\n"
        "1. Подготовлен и проверен автономный набор из 22 юнит-тестов для собственного метода регистрации пользователей (ЛР1).\n"
        "2. Проанализирован предоставленный модуль расчета доставки (Delivery.py), восстановлены бизнес-требования к логике расчета стоимости и сроков транспортировки.\n"
        "3. Разработан набор из 23 юнит-тестов для модуля доставки, покрывающий все классы эквивалентности и граничные значения.\n"
        "4. Зафиксированы и локализованы дефекты, приводящие к падению тестов на предоставленном коде доставки."
    )

    # --- 2. ПУНКТ А ---
    h2 = doc.add_heading("2. Пункт А: Общее количество тестов и итоговая статистика прохождения", level=1)
    h2.style.font.name = 'Times New Roman'
    h2.style.font.size = Pt(14)
    h2.style.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    doc.add_paragraph(
        "Всего в рамках лабораторной работы разработано 45 юнит-тестов, разделенных на два независимых тестовых модуля:"
    )

    # Таблица статистики
    table_stat = doc.add_table(rows=4, cols=6)
    table_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_stat.style = 'Table Grid'

    headers = [
        "Тестируемый модуль",
        "Файл тестов",
        "Всего тестов",
        "Пройдено (OK)",
        "Упало (Fail/Err)",
        "Успешность"
    ]
    for i, h in enumerate(headers):
        cell = table_stat.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1F3864")
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_stat = [
        ("ЛР1: Регистрация пользователей", "test_registration.py", "22", "22", "0", "100.0%"),
        ("ЛР2: Модуль расчета доставки", "test_delivery.py", "23", "19", "4", "82.6%"),
        ("ИТОГО ПО ПРОЕКТУ", "Все модули", "45", "41", "4", "91.1%")
    ]

    for row_idx, row_data in enumerate(data_stat, start=1):
        bg_col = "F2F4F7" if row_idx % 2 == 1 else "FFFFFF"
        if row_idx == 3:
            bg_col = "D9E1F2"
        for col_idx, val in enumerate(row_data):
            cell = table_stat.cell(row_idx, col_idx)
            cell.text = val
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            if col_idx in [2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(10)
                if row_idx == 3:
                    run.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "Характеристика тестов собственного проекта (test_registration.py):\n"
        "• 22 теста полностью покрывают все правила валидации учетных данных: корректность телефонных масок, "
        "RFC-структуру адресов электронной почты, ограничения длины и допустимых символов строковых логинов, "
        "проверку по черному списку системных имен, а также многокритериальную валидацию пароля (кириллица, оба регистра, "
        "наличие цифр и спецсимволов) и сквозное маскирование через детерминированный SHA-256.\n"
        "• Все 22 теста завершаются успешно (status OK), подтверждая отсутствие регрессионных дефектов."
    )

    doc.add_paragraph(
        "Характеристика тестов модуля доставки (test_delivery.py):\n"
        "• 23 теста охватывают расчет базового тарифа (200 руб.), километража (5 руб./км), весовые надбавки "
        "(1.2 при весе > 5 кг; 1.5 при весе >= 20 кг), надбавки по категории («хрупкий» +300 руб., «опасный» +1000 руб.), "
        "расчет календарных сроков транспортировки от фиксированной даты (2026-09-03), граничные значения (0.1 кг, 50.0 кг, "
        "1 км, 5000 км), а также недопустимые физические параметры грузов."
    )

    # --- 3. ПУНКТ Б ---
    h3 = doc.add_heading("3. Пункт Б: Количество упавших тестов для модуля доставки (Delivery.py)", level=1)
    h3.style.font.name = 'Times New Roman'
    h3.style.font.size = Pt(14)
    h3.style.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    doc.add_paragraph(
        "При прогоне набора тестов test_delivery.py на предоставленном исходном коде Delivery.py зафиксировано:\n"
        "• Точное количество упавших тестов: 4 (четыре).\n"
        "• Из них с ошибкой проверки утверждения (AssertionError / FAIL): 3 теста.\n"
        "• Из них с необработанным исключением исполнения (TypeError / ERROR): 1 тест."
    )

    doc.add_paragraph("Список упавших тестов и характер ошибок:")
    fails = [
        ("test_express_delivery_cost_surcharge (FAIL)",
         "AssertionError: 350 not greater than 700. Ожидалось, что экспресс-доставка будет стоить дороже базового тарифа, "
         "однако в коде стоимость уменьшилась в 2 раза (скидка вместо наценки)."),
        ("test_express_delivery_minimum_one_day (FAIL)",
         "AssertionError: '2026-09-03' != '2026-09-04'. При коротких дистанциях срок доставки составил 0 дней (день в день с отправкой), "
         "что нарушает ограничение на минимальный срок транспортировки."),
        ("test_package_type_case_insensitivity (FAIL)",
         "AssertionError: -1 != 700. Передача типа 'Обычный' с заглавной буквы привела к ложному отказу (-1, '0000-00-00') "
         "из-за регистрозависимого сравнения."),
        ("test_invalid_input_types_graceful_handling (ERROR)",
         "TypeError: '<' not supported between instances of 'str' and 'float'. При передаче строки 'десять' вместо числа "
         "произошло аварийное падение функции вместо возврата кода ошибки.")
    ]

    for title, desc in fails:
        p_fail = doc.add_paragraph()
        r_f1 = p_fail.add_run(f"❌ {title}\n")
        r_f1.font.bold = True
        r_f1.font.color.rgb = RGBColor(0x9C, 0x00, 0x06)
        r_f2 = p_fail.add_run(f"Детали: {desc}")
        r_f2.font.size = Pt(11)

    # --- 4. ПУНКТ В ---
    h4 = doc.add_heading("4. Пункт В: Локализация аномалий и дефектов в коде Delivery.py", level=1)
    h4.style.font.name = 'Times New Roman'
    h4.style.font.size = Pt(14)
    h4.style.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    doc.add_paragraph(
        "В таблице ниже представлена подробная локализация обнаруженных аномалий с указанием номеров строк, "
        "описания дефектов в логике разработчика и предложенных исправлений."
    )

    # Таблица локализации дефектов
    table_bugs = doc.add_table(rows=5, cols=4)
    table_bugs.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_bugs.style = 'Table Grid'

    col_widths = [Inches(1.8), Inches(0.8), Inches(2.3), Inches(2.1)]

    b_headers = ["Название теста", "Строка", "Описание дефекта", "Вариант исправления"]
    for i, h in enumerate(b_headers):
        cell = table_bugs.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1F3864")
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    bugs_data = [
        (
            "test_express_delivery_cost_surcharge",
            "36",
            "Дефект в расчете экспресс-доставки: разработчик применил умножение на 0.5 (total_cost *= 0.5), что дает скидку 50% вместо наценки за срочность услуги.",
            "if is_express:\n    total_cost *= 1.5\n# (или *= 2.0 / +500 руб. в зависимости от тарифа)"
        ),
        (
            "test_express_delivery_minimum_one_day",
            "44",
            "Логическая ошибка деления: при days_needed == 1 (для расстояний < 1000 км) операция 1 // 2 дает 0 дней, приводя к нереалистичной моментальной доставке в день отправки.",
            "if is_express:\n    days_needed = max(1, days_needed // 2)\n# гарантирует мин. срок 1 день"
        ),
        (
            "test_package_type_case_insensitivity",
            "16",
            "Отсутствие нормализации строки: проверка 'package_type not in valid_types' чувствительна к регистру. Значения 'Обычный', 'Хрупкий' приводят к ошибке.",
            "clean_type = str(package_type).strip().lower()\nif clean_type not in valid_types:\n    return -1, '0000-00-00'"
        ),
        (
            "test_invalid_input_types_graceful_handling",
            "12",
            "Отсутствие типовой валидации: передача строковых значений или None приводит к аварийному исключению TypeError при сравнении weight < 0.1, нарушая контракт метода.",
            "if not isinstance(weight, (int, float)) or not isinstance(distance, int) or isinstance(distance, bool):\n    return -1, '0000-00-00'"
        )
    ]

    for row_idx, data in enumerate(bugs_data, start=1):
        bg_col = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = table_bugs.cell(row_idx, col_idx)
            cell.text = text
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            if col_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(9.5)
                if col_idx == 0:
                    run.font.bold = True
                elif col_idx == 3:
                    run.font.name = 'Consolas'
                    run.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- 5. ВЫВОДЫ ---
    h5 = doc.add_heading("5. Заключение", level=1)
    h5.style.font.name = 'Times New Roman'
    h5.style.font.size = Pt(14)
    h5.style.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    doc.add_paragraph(
        "В результате выполнения лабораторной работы №2 была продемонстрирована высокая эффективность юнит-тестирования "
        "как метода контроля качества программного обеспечения. Разработанный комплекс из 45 тестов позволил не только "
        "подтвердить стабильность и надежность ранее разработанного собственного модуля регистрации пользователей (ЛР1), "
        "но и быстро выявить 4 критических дефекта в стороннем модуле расчета доставки (Delivery.py), включающие ошибки бизнес-логики, "
        "краевые эффекты целочисленного деления и отсутствие безопасной обработки нетипизированных входных данных."
    )

    output_path = "Отчет_ЛР2_Романов_Р_О.docx"
    doc.save(output_path)
    print(f"Отчет успешно создан: {output_path}")


if __name__ == "__main__":
    create_report()
