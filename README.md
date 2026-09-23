<div align="center">

# 🟢 OldClockWidget

### LED-style desktop clock & drawing widget for Windows

**Українська** · [English](#english)

<img src="assets/old-clock-widget.png" alt="OldClockWidget screenshot" width="100%">

<br>

`Windows 10/11` · `Python` · `PySide6` · `PyInstaller`

</div>

---

# 🇺🇦 Українська

**OldClockWidget** — легкий настільний віджет-годинник для Windows у стилі старого LED-дисплея.  
Він використовує власний dot-matrix шрифт, підтримує малювання прямо на LED-матриці та працює без зайвих елементів інтерфейсу.

Віджет **не відображається на панелі завдань і не створює іконку в системному треї** — на робочому столі залишається тільки сам годинник.

## ✨ Можливості

- 🕒 Живий час у форматі `HH:MM:SS`
- 💚 Власний зелений LED dot-matrix шрифт
- 🌑 Темна матриця неактивних LED-точок
- 🎨 Малювання кольоровими LED
- 🖌️ Окрема зона малювання справа
- ✏️ Малювання на LED-рамці навколо годинника
- 🧽 Стирання правою кнопкою миші
- 🌈 9 кольорів для малювання
- 📐 Зміна розміру віджета
- 🖱️ Перетягування в будь-яке місце робочого столу
- 🔒 **Lock** — блокує переміщення та зміну розміру
- 📌 **Always on top**
- 🚀 **Start with Windows**
- 👁️ Можна приховати бокову зону малювання
- ✍️ Можна приховати підпис `Created by Ivan Roliuk`
- 💾 Автоматичне збереження позиції, розміру, малюнка та налаштувань
- 🫥 Немає іконки в треї
- 🪟 Немає кнопки на панелі завдань

> Область самого часу захищена від малювання. Малювати можна лише на LED-рамці навколо годинника та в окремій зоні справа.

## 🖱️ Керування

| Дія | Результат |
|---|---|
| ЛКМ + перетягування по вільній області | Перемістити віджет |
| Нижній правий кут | Змінити розмір |
| ЛКМ по доступних LED | Малювати |
| ПКМ по доступних LED | Стирати |
| ПКМ поза зоною малювання | Відкрити меню |
| `Drawing panel` | Показати / приховати бокову панель |
| `Drawing color` | Вибрати колір |
| `Clear drawing` | Очистити малюнок |
| `Lock` | Заблокувати позицію та розмір |
| `Always on top` | Поверх інших вікон |
| `Start with Windows` | Автозапуск разом із Windows |
| `Reset size` | Повернути стандартний розмір |
| `Exit` | Зберегти стан і закрити |

## 🚀 Запуск із вихідного коду

Потрібні **Windows 10/11** та **Python 3**.

```bash
git clone https://github.com/irolyuk/OldClockWidget.git
cd OldClockWidget
```

Після цього запусти:

```bat
run.bat
```

Скрипт сам перевірить наявність `PySide6` та встановить його за потреби.

Або вручну:

```bash
py -m pip install PySide6
py main.py
```

## 📦 Збірка `.exe`

Запусти:

```bat
build.bat
```

`build.bat` встановить потрібні залежності та збере програму через PyInstaller.

Готовий файл:

```text
dist\OldClockWidget.exe
```

`clock_font.json` автоматично додається всередину збірки.

## 💾 Збереження налаштувань

OldClockWidget використовує Qt `QSettings`:

```text
Organization: IvanRoliuk
Application: OldClockWidget
```

Між запусками зберігаються позиція та розмір вікна, малюнок, вибраний колір, видимість панелі, видимість підпису та стан `Lock`.

`Start with Windows` використовує Run-ключ поточного користувача Windows і **не потребує прав адміністратора**.

## 📁 Структура

```text
OldClockWidget/
├── assets/
│   └── old-clock-widget.png
├── main.py
├── clock_font.json
├── requirements.txt
├── run.bat
├── build.bat
├── README.md
└── LICENSE
```

---

# English

**OldClockWidget** is a lightweight LED-style desktop clock widget for Windows.  
It uses a custom dot-matrix font, supports drawing directly on the LED matrix, and keeps the desktop experience clean and minimal.

The widget has **no taskbar button and no system tray icon** — only the clock itself stays visible on the desktop.

## ✨ Features

- 🕒 Real-time `HH:MM:SS` clock
- 💚 Custom green LED dot-matrix font
- 🌑 Dark inactive LED matrix
- 🎨 Multicolor LED drawing
- 🖌️ Dedicated drawing panel
- ✏️ Drawing on the LED border around the clock
- 🧽 Right-click erasing
- 🌈 9 drawing colors
- 📐 Resizable widget
- 🖱️ Drag anywhere on the desktop
- 🔒 **Lock** mode prevents moving and resizing
- 📌 **Always on top**
- 🚀 **Start with Windows**
- 👁️ Hide/show the side drawing panel
- ✍️ Hide/show the `Created by Ivan Roliuk` signature
- 💾 Persistent position, size, drawings and settings
- 🫥 No system tray icon
- 🪟 No taskbar entry

> The clock area itself is protected from drawing. LEDs can be drawn only on the border surrounding the clock and inside the dedicated side panel.

## 🖱️ Controls

| Action | Result |
|---|---|
| Left-drag empty area | Move widget |
| Bottom-right corner | Resize |
| Left-click / drag drawable LEDs | Draw |
| Right-click / drag drawable LEDs | Erase |
| Right-click elsewhere | Open menu |
| `Drawing panel` | Show / hide side panel |
| `Drawing color` | Select drawing color |
| `Clear drawing` | Clear drawing |
| `Lock` | Lock position and size |
| `Always on top` | Keep above other windows |
| `Start with Windows` | Enable Windows startup |
| `Reset size` | Restore default size |
| `Exit` | Save state and close |

## 🚀 Run from source

Requires **Windows 10/11** and **Python 3**.

```bash
git clone https://github.com/irolyuk/OldClockWidget.git
cd OldClockWidget
```

Then run:

```bat
run.bat
```

The script checks for `PySide6` and installs it automatically if necessary.

Or run manually:

```bash
py -m pip install PySide6
py main.py
```

## 📦 Build standalone `.exe`

Run:

```bat
build.bat
```

The script installs the required build dependencies and creates a single-file windowed executable with PyInstaller.

Output:

```text
dist\OldClockWidget.exe
```

`clock_font.json` is bundled automatically.

## 💾 Persistent settings

OldClockWidget uses Qt `QSettings`:

```text
Organization: IvanRoliuk
Application: OldClockWidget
```

Window position and size, drawings, selected drawing color, panel visibility, signature visibility, and the `Lock` state are preserved between launches.

The **Start with Windows** option uses the current user's Windows Run registry key and **does not require administrator privileges**.

## 📁 Project structure

```text
OldClockWidget/
├── assets/
│   └── old-clock-widget.png
├── main.py
├── clock_font.json
├── requirements.txt
├── run.bat
├── build.bat
├── README.md
└── LICENSE
```

---

## 📄 License

Released under the **MIT License**. See [`LICENSE`](LICENSE).

## 👤 Author

**Ivan Roliuk**

Created with a custom LED font originally designed for OldClockWidget.
