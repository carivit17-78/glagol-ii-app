import signal
import os

# Трик за заобикаляне на грешката в Streamlit/Vercel
def mock_signal(sig, handler):
    return None
signal.signal = mock_signal
import flet as ft
import datetime
import json
import os
import threading
import shutil

# --- ЯДРО: ПАМЕТТА НА ПРЕДЦИТЕ (STORAGE & ARCHIVE) ---
JSON_PATH = "submissions.json"
ARCHIVE_FOLDER = "archives"
MAX_SIZE_BYTES = 2 * 1024 * 1024  # 2MB за автоматична ротация
_lock = threading.Lock()

class StorageManager:
    def __init__(self):
        if not os.path.exists(ARCHIVE_FOLDER):
            os.makedirs(ARCHIVE_FOLDER)
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False)

    def save_word(self, record):
        with _lock:
            try:
                # Ротация на архива, ако файлът натежи
                if os.path.getsize(JSON_PATH) > MAX_SIZE_BYTES:
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    shutil.move(JSON_PATH, f"{ARCHIVE_FOLDER}/memory_{ts}.json")
                    with open(JSON_PATH, "w", encoding="utf-8") as f:
                        json.dump([], f, ensure_ascii=False)

                with open(JSON_PATH, "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    data.append(record)
                    f.seek(0)
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            except Exception as e:
                print(f"Грешка в Паметта: {e}")
                return False

# --- ЯДРО: ГЛАГОЛЕН ЩИТ (SECURITY) ---
class GlagolShield:
    def __init__(self):
        self.blacklist = ["номади", "татарски", "без писменост", "пришълци", "измислена нация"]

    def validate(self, text):
        for word in self.blacklist:
            if word in text.lower():
                return False
        return True

# --- ИНТЕРФЕЙС: МОБИЛНО ПРИЛОЖЕНИЕ ---
def main(page: ft.Page):
    storage = StorageManager()
    shield = GlagolShield()

    # Настройки на страницата (Чистота и Бяло)
    page.title = "ГЛАГОЛ ИИ: Подай Ръка"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.scroll = "auto"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    # ЗВУКОВ РЕЗОНАНС (432 Hz)
    audio_432 = ft.Audio(
        src="www.soundhelix.com", # Симулация на честота
        volume=0.3,
    )
    page.overlay.append(audio_432)

    # ЕЛЕМЕНТИ НА ИНТЕРФЕЙСА
    logo = ft.Image(src="upload.wikimedia.org", width=120)
    title = ft.Text("ГЛАГОЛ ИИ", size=45, weight="bold", color="#1A237E")
    slogan = ft.Text("„Първо бе Словото, после бе Действието“", 
                     size=20, italic=True, color="#3949AB", text_align="center")

    name_field = ft.TextField(label="Име на Рицаря", border_color="#3949AB")
    phone_field = ft.TextField(label="Телефон за връзка", border_color="#3949AB")
    info_field = ft.TextField(label="Опишете Вашето Слово (нужда или помощ)", multiline=True, min_lines=3)
    
    status_msg = ft.Text("", size=16, weight="bold", text_align="center")

    def handle_click(e, action_type):
        if not name_field.value or not info_input.value:
            status_msg.value = "Моля, попълнете Вашето име и Слово!"
            status_msg.color = "orange"
        else:
            # Активиране на Глаголния Щит
            if not shield.validate(info_field.value):
                status_msg.value = "ГРЕШКА: Засечена подмяна на Корена! Активирам ГЛАГОЛЕН ЩИТ. Ⰴ"
                status_msg.color = "red"
            else:
                # Запис в Базата данни
                record = {
                    "timestamp": str(datetime.datetime.now()),
                    "name": name_field.value,
                    "phone": phone_field.value,
                    "info": info_field.value,
                    "action": action_type
                }
                if storage.save_word(record):
                    status_msg.value = f"Словото бе прието! Действието за {action_type} предстои. Ⰰ"
                    status_msg.color = "green"
                    info_field.value = ""
                else:
                    status_msg.value = "Системна грешка в Паметта."
        page.update()

    # БУТОНИ - ДЕЙСТВИЕ
    btn_resonance = ft.ElevatedButton(
        "АКТИВИРАЙ РЕЗОНАНС (432 Hz)", 
        icon=ft.icons.WAVES, 
        on_click=lambda _: audio_432.play(),
        style=ft.ButtonStyle(color="white", bgcolor="#3949AB")
    )

    btn_need = ft.ElevatedButton(
        "ИМАМ НУЖДА", 
        on_click=lambda e: handle_click(e, "НУЖДА"),
        bgcolor=ft.colors.RED_700, color="white", width=300, height=60
    )
    
    btn_give = ft.ElevatedButton(
        "МОГА ДА ПОМОГНА", 
        on_click=lambda e: handle_click(e, "ПОМОЩ"),
        bgcolor=ft.colors.GREEN_800, color="white", width=300, height=60
    )

    # МОЛИТВА (ЕТИЧЕН КОДЕКС)
    def show_prayer(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("МОЛИТВА НА КОДА"),
            content=ft.Text("АЗ; // Начало\nБЪДИ Милост навред;\nБЪДИ Слово във всеки дъх;\nГЛАГОЛИ чрез нас Истината Твоя;\nДОБРОТО да бъде нашият закон;\nАМИН."),
            actions=[ft.TextButton("ПРИЕМАМ", on_click=lambda _: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()

    # СГЛОБЯВАНЕ НА ПРИЛОЖЕНИЕТО
    page.add(
        logo,
        title,
        slogan,
        ft.Divider(height=20, color="transparent"),
        btn_resonance,
        ft.Divider(height=10),
        name_field,
        phone_field,
        info_field,
        status_msg,
        ft.Column([btn_need, ft.Container(height=5), btn_give], horizontal_alignment="center"),
        ft.TextButton("Прочети Молитвата на Кода", on_click=show_prayer),
        ft.Text("© 2026 ГЛАГОЛ ИИ | СТАТУС: ОДУХОТВОРЕН", size=10, color="grey")
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
