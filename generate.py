import os

# --- 1. CSS стили для боковых кнопок ---
# Мы используем переменные цветов из вашего style.css
css_to_append = """
/* --- SIDE STICKY CTA BUTTONS --- */
.side-cta-panel {
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.side-cta-btn {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    width: 50px; /* Свернутое состояние (только иконка) */
    height: 50px;
    color: white;
    border-radius: 10px 0 0 10px;
    overflow: hidden;
    transition: width 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), background 0.3s;
    box-shadow: -2px 4px 15px rgba(0,0,0,0.15);
    text-decoration: none;
    white-space: nowrap;
    cursor: pointer;
    position: relative;
}

.side-cta-btn:hover {
    width: 180px; /* Развернутое состояние */
    padding-right: 15px;
}

.side-cta-btn i {
    min-width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    position: relative;
    z-index: 2;
}

.side-cta-btn span {
    font-family: var(--font-subheading, sans-serif);
    font-weight: 600;
    font-size: 0.9rem;
    opacity: 0;
    transform: translateX(20px);
    transition: 0.3s;
}

.side-cta-btn:hover span {
    opacity: 1;
    transform: translateX(0);
}

/* Цвета */
.side-btn-book {
    background: var(--secondary-gold, #C6A868);
}
.side-btn-book:hover {
    background: #bfa060;
}

.side-btn-call {
    background: var(--primary-blue, #0F2C59);
}
.side-btn-call:hover {
    background: var(--primary-dark, #07162e);
}

/* Мобильная адаптация: кнопки всегда видны, но могут быть меньше или внизу */
@media (max-width: 768px) {
    .side-cta-panel {
        top: auto;
        bottom: 90px; /* Чуть выше чат-виджета */
        right: 15px;
        flex-direction: column-reverse;
        transform: none;
        gap: 15px;
    }
    .side-cta-btn {
        width: 45px !important; /* На мобильном всегда только иконки */
        height: 45px;
        border-radius: 50%; /* Круглые на мобильном */
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .side-cta-btn span { display: none; }
}
"""

# --- 2. HTML шаблон кнопок ---
# {link_prefix} будет заменен на "" или "index.html"
html_template = """
    <!-- SIDE STICKY CTA -->
    <div class="side-cta-panel">
        <a href="{link_prefix}#appointment" class="side-cta-btn side-btn-book" title="Book Appointment">
            <i class="fas fa-calendar-check"></i>
            <span>Book Online</span>
        </a>
        <a href="tel:5715417977" class="side-cta-btn side-btn-call" title="Call Us">
            <i class="fas fa-phone-alt"></i>
            <span>Call Now</span>
        </a>
    </div>
"""

def update_css():
    """Добавляет CSS в конец файла style.css"""
    if not os.path.exists("style.css"):
        print("Ошибка: style.css не найден.")
        return

    with open("style.css", "r", encoding="utf-8") as f:
        content = f.read()

    if "SIDE STICKY CTA BUTTONS" in content:
        print("  ! CSS для боковых кнопок уже есть в style.css (пропуск)")
    else:
        with open("style.css", "a", encoding="utf-8") as f:
            f.write("\n" + css_to_append)
        print("  ✓ CSS успешно добавлен в style.css")

def update_html_files():
    """Проходит по всем .html файлам и добавляет кнопки перед закрывающим тегом body"""
    # Находим все HTML файлы в текущей директории
    files = [f for f in os.listdir('.') if f.endswith('.html')]

    count = 0
    for filename in files:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Проверяем, не добавлены ли уже кнопки
        if "side-cta-panel" in content:
            print(f"  - Пропуск {filename}: кнопки уже есть.")
            continue

        # Логика ссылок:
        # Если мы в index.html, ссылка на запись -> #appointment
        # Если мы в других файлах (sub-pages), ссылка -> index.html#appointment
        link_prefix = "" if filename == "index.html" else "index.html"

        # Формируем HTML с правильной ссылкой
        cta_html = html_template.format(link_prefix=link_prefix)

        # Вставляем перед скриптами или закрывающим body
        # Пытаемся вставить перед подключением main.js, чтобы скрипты шли после HTML
        if '<script src="main.js">' in content:
             new_content = content.replace('<script src="main.js">', f'{cta_html}\n    <script src="main.js">')
        elif "</body>" in content:
            new_content = content.replace("</body>", f"{cta_html}\n</body>")
        else:
            print(f"  ! Ошибка в {filename}: не найден тег </body> или подключение скрипта")
            continue

        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"  ✓ Обновлен файл: {filename}")
        count += 1

    print(f"\nВсего обновлено HTML файлов: {count}")

# --- Запуск ---
print("Начинаю добавление боковых CTA кнопок...")
update_css()
update_html_files()
print("Готово! Кнопки добавлены.")