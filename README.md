# 🕷️ MitMToolkit - Комплексный инструмент для тестирования Man-in-the-Middle атак

![MitMToolkit](https://img.shields.io/badge/Version-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Linux](https://img.shields.io/badge/Linux-Fedora%20%7C%20Kali%20%7C%20Ubuntu-red)
![License](https://img.shields.io/badge/License-MIT-blue)
![Security](https://img.shields.io/badge/Security-Penetration%20Testing-orange)

**Мощный инструмент для тестирования Man-in-the-Middle атак с поддержкой ARP и DNS спуфинга** 🌐

![Скриншот интерфейса main.py](https://raw.githubusercontent.com/DenisPythoneer/MitMToolkit/main/image/screenshotOne.png)

---

## 📖 Описание

**MitMToolkit** - это профессиональный инструмент для проведения тестов на проникновение и анализа сетевой безопасности. Предоставляет комплексные возможности для моделирования атак "человек посередине" в контролируемых условиях.

### Проект включает два основных модуля атак:
- **ARP Spoofing** - перехват сетевого трафика через подмену ARP-таблиц
- **DNS Spoofing** - манипуляция DNS-запросами для перенаправления трафика

### Идеально подходит для:
- Тестирования на проникновение 🔓
- Анализа уязвимостей сети
- Образовательных целей и исследований
- Проверки защищенности сетевой инфраструктуры

---

## ✨ Основные возможности

### 🔍 ARP Spoofing
- **Перехват трафика** между узлами сети
- **Манипуляция ARP-таблицами** для перенаправления пакетов
- **Поддержка различных сетевых конфигураций**

![Скриншот интерфейса ARP.py](https://raw.githubusercontent.com/DenisPythoneer/MitMToolkit/main/image/screenshotTwo.png)

### 🌐 DNS Spoofing  
- **Подмена DNS-запросов** в реальном времени
- **Перенаправление доменных имен** на указанные IP-адреса
- **Гибкая настройка правил подмены**

![Скриншот интерфейса DNS.py](https://raw.githubusercontent.com/DenisPythoneer/MitMToolkit/main/image/screenshotThree.png)

### 💻 Профессиональный интерфейс
- **Цветной консольный интерфейс** с ASCII-графикой
- **Интуитивное меню** выбора типа атаки
- **Детальная информация** о процессе выполнения

### 🛡️ Безопасность и контроль
- **Требует права root** для работы с сетевыми интерфейсами
- **Четкие предупреждения** о предназначении для образовательных целей
- **Контроль ошибок** и обработка исключений

---

## 🛠 Технологии

### Backend
- **Python 3.8+** - основной язык программирования
- **Colorama** - цветной вывод в консоль
- **Subprocess** - управление внешними процессами

### Сетевые возможности
- **Raw socket manipulation** - работа с сетевыми пакетами
- **ARP protocol handling** - манипуляция ARP-запросами
- **DNS packet processing** - обработка DNS-трафика

---

## ⚡ Быстрый старт

### **Клонирование репозитория:**
```bash
git clone https://github.com/DenisPythoneer/MitMToolkit.git
cd MitMToolkit
```

### Установка зависимостей
```bash
pip3 install -r requirements.txt
```

### Запуск программы
```bash
sudo python3 main.py
```
---

### ⚠️ Важное предупреждение
- **Только для легального использования!**

---

## 🏗️ Структура проекта
```text
MitMToolkit/
├── main.py                # Основной запускаемый файл
├── ARP-Spoofing/
│   └── ARP.py             # Модуль ARP спуфинга
├── DNS-Spoofing/
│   └── DNS.py             # Модуль DNS спуфинга
├── README.md              # Документация
│
└── requirements.txt       # Библиотеки
```
---

### 🔧 Требования
- **Python 3.8+**
- **Права root/sudo**
- **Linux/Unix система**
- **Сетевой интерфейс с поддержкой promiscuous mode**

---

## 🔗 Ссылка на автора: https://github.com/DenisPythoneer
