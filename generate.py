import os
import re

# 1. Список услуг (названия файлов будут сгенерированы автоматически)
services_list = [
    "Dental Implants",
    "All-on-4 Implants",
    "Dental Crowns",
    "Dental Bridges",
    "Dentures",
    "Invisalign",
    "Teeth Whitening",
    "Dental Sealants",
    "Dental Bonding",
    "Porcelain Veneers",
    "Braces",
    "Gum Graft",
    "Root Canal",
    "Pediatric Dentistry",
    "Emergency Dentist",
    "Dental Fillings",
    "Dental X-Rays",
    "Tooth Extraction",
    "Sedation Dentistry",
    "TMJ Therapy",
    "Bruxism Treatment",
    "Sleep Apnea"
]

# 2. Текст-рыба (Lorem Ipsum)
lorem_short = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
lorem_long = "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."

# 3. Чтение исходного index.html для извлечения общих частей
try:
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()
except FileNotFoundError:
    print("ОШИБКА: Файл index.html не найден. Пожалуйста, положите скрипт в папку с сайтом.")
    exit()

# --- Извлечение частей ---

# Извлекаем <head> (метатеги, стили)
# Мы немного модифицируем head, чтобы добавить стили для внутренних страниц
head_match = re.search(r"<head>(.*?)</head>", index_content, re.DOTALL)
head_content = head_match.group(1) if head_match else ""

# Добавляем CSS специально для внутренних страниц (Internal Hero)
internal_css = """
    <style>
        /* Specific Styles for Generated Pages */
        .internal-hero {
            position: relative;
            height: 40vh;
            min-height: 400px;
            background: linear-gradient(135deg, var(--primary-blue), var(--primary-dark));
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-top: -80px; /* Counteract sticky header spacing */
            padding-top: 80px;
            overflow: hidden;
        }
        .internal-hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
            opacity: 0.2;
            mix-blend-mode: overlay;
        }
        .internal-hero-content {
            position: relative;
            z-index: 2;
            color: white;
            padding: 0 20px;
        }
        .internal-hero h1 {
            color: white;
            font-size: 3.5rem;
            margin-bottom: 20px;
        }
        .breadcrumbs {
            font-family: var(--font-subheading);
            font-size: 0.9rem;
            color: var(--secondary-gold);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .breadcrumbs a { color: rgba(255,255,255,0.7); }
        .breadcrumbs a:hover { color: white; }
    </style>
"""

# Извлекаем Header (Навигация)
header_match = re.search(r"(<header class=\"main-header\">.*?</header>)", index_content, re.DOTALL)
header_content = header_match.group(1) if header_match else ""

# В навигации нужно заменить ссылки якоря (#about) на полные (index.html#about),
# так как мы будем на другой странице
header_content = header_content.replace('href="#', 'href="index.html#')
# Логотип должен вести на главную
header_content = header_content.replace('href="#" class="logo"', 'href="index.html" class="logo"')

# Извлекаем Footer
footer_match = re.search(r"(<footer.*</footer>)", index_content, re.DOTALL)
footer_content = footer_match.group(1) if footer_match else ""
# Исправляем ссылки в футере тоже
footer_content = footer_content.replace('href="#', 'href="index.html#')

# Извлекаем виджеты (Accessibility, Chat) и скрипты в конце body
# Ищем все от конца футера до закрывающего body
widgets_match = re.search(r"</footer>(.*?)</body>", index_content, re.DOTALL)
widgets_scripts = widgets_match.group(1) if widgets_match else ""
# Ссылки в скриптах менять не надо, так как файлы лежат в той же папке

# 4. Функция генерации страницы
def generate_page(service_name):
    # Создаем имя файла (slug)
    slug = service_name.lower().replace(" ", "-") + ".html"

    # HTML Шаблон
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    {head_content}
    <title>{service_name} | Lorton Dentist VA</title>
    <meta name="description" content="Professional {service_name} services in Lorton, VA. Top rated dental care for your family.">
    {internal_css}
</head>
<body>

    {header_content}

    <main>
        <section class="internal-hero">
            <div class="internal-hero-content fade-in-up">
                <div class="breadcrumbs">
                    <a href="index.html">Home</a> <i class="fas fa-chevron-right" style="font-size: 0.7em; margin: 0 10px;"></i> <span>Services</span>
                </div>
                <h1>{service_name}</h1>
                <p style="color: rgba(255,255,255,0.9); max-width: 600px; margin: 0 auto;">
                    Professional dental care designed for your comfort and long-term health.
                </p>
                <a href="index.html#appointment" class="btn btn-pulse" style="margin-top: 30px;">Book Appointment</a>
            </div>
        </section>

        <section class="container split-section fade-in-up" style="padding: 80px 24px;">
            <div class="split-text">
                <h3 class="section-tag">Overview</h3>
                <h2>About {service_name}</h2>
                <div class="divider align-left"></div>
                <p>{lorem_short}</p>
                <p>{lorem_long}</p>

                <ul class="feature-list">
                    <li><i class="fas fa-check"></i> Comprehensive exam included</li>
                    <li><i class="fas fa-check"></i> Latest dental technology</li>
                    <li><i class="fas fa-check"></i> Experienced specialists</li>
                </ul>
            </div>
            <div class="split-img-wrapper">
                <div class="split-img">
                    <img src="https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=800&q=80"
                         alt="{service_name}" width="600" height="400">
                </div>
            </div>
        </section>

        <section class="bg-grey" style="padding: 80px 0;">
            <div class="container fade-in-up">
                <div class="text-center" style="max-width: 800px; margin: 0 auto;">
                    <h3 class="section-tag">Procedure</h3>
                    <h2>What to Expect</h2>
                    <div class="divider"></div>
                    <p>{lorem_long}</p>
                </div>

                <div class="services-modern-grid" style="margin-top: 50px;">
                    <div class="special-card" style="background: white; color: var(--text-main); border: 1px solid #eee;">
                        <div class="card-icon"><i class="fas fa-user-md"></i></div>
                        <h4 style="color: var(--primary-blue);">Consultation</h4>
                        <p style="color: var(--text-light);">We start with a thorough examination to determine the best course of action for your specific needs.</p>
                    </div>
                    <div class="special-card" style="background: white; color: var(--text-main); border: 1px solid #eee;">
                        <div class="card-icon"><i class="fas fa-tools"></i></div>
                        <h4 style="color: var(--primary-blue);">Treatment</h4>
                        <p style="color: var(--text-light);">{lorem_short[:100]}...</p>
                    </div>
                    <div class="special-card" style="background: white; color: var(--text-main); border: 1px solid #eee;">
                        <div class="card-icon"><i class="fas fa-smile"></i></div>
                        <h4 style="color: var(--primary-blue);">Aftercare</h4>
                        <p style="color: var(--text-light);">We provide detailed instructions to ensure a quick recovery and lasting results.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="bg-blue text-white" style="padding: 80px 0; text-align: center; position: relative; overflow: hidden;">
            <div class="bg-circle"></div>
            <div class="container fade-in-up" style="position: relative; z-index: 2;">
                <h3 class="section-tag white">Take the Next Step</h3>
                <h2 class="text-white">Ready for a Healthy Smile?</h2>
                <div class="divider bg-white" style="opacity: 0.8;"></div>
                <p class="text-white" style="max-width: 600px; margin: 0 auto 40px;">
                    Schedule your visit for {service_name} today. We are accepting new patients in Lorton, VA.
                </p>
                <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                    <a href="index.html#appointment" class="btn btn-gold-solid">Book Appointment</a>
                    <a href="tel:5715417977" class="btn btn-white-outline">Call 571-541-7977</a>
                </div>
            </div>
        </section>

    </main>

    {footer_content}
    {widgets_scripts}

</body>
</html>
    """

    # Записываем файл
    with open(slug, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ Создана страница: {slug}")

# 5. Запуск цикла
print("Начинаю генерацию страниц...")
for service in services_list:
    generate_page(service)

print("\nГотово! Все страницы сгенерированы.")