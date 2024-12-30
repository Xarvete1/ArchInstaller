import subprocess

def run_command(command):
    """Запуск системной команды"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
        exit(1)

def select_disk():
    """Выбор диска для установки"""
    disk = input("Введите диск для установки (например, /dev/sda): ")
    return disk

def partition_disk(disk):
    """Разметка диска"""
    print(f"Создаем таблицу разделов GPT на {disk}...")
    run_command(f"parted {disk} --script mklabel gpt")
    print("Создаем основной раздел f2fs...")
    run_command(f"parted {disk} --script mkpart primary f2fs 1MiB 100%")

def format_partition(disk):
    """Форматирование раздела"""
    partition = f"{disk}1"
    print(f"Форматируем раздел {partition} в f2fs...")
    run_command(f"mkfs.f2fs {partition}")

def mount_partition(disk):
    """Монтирование раздела"""
    partition = f"{disk}1"
    print(f"Монтируем раздел {partition} в /mnt...")
    run_command(f"mount {partition} /mnt")

def install_base_system():
    """Установка базовой системы"""
    print("Устанавливаем базовую систему Arch Linux...")
    run_command("pacstrap /mnt base linux linux-firmware")

def generate_fstab():
    """Генерация fstab"""
    print("Генерируем fstab...")
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")

def setup_arch():
    """Основная функция установки"""
    print("Добро пожаловать в ArchInstaller!")
    
    disk = select_disk()
    partition_disk(disk)
    format_partition(disk)
    mount_partition(disk)
    install_base_system()
    generate_fstab()

    print("Базовая система установлена успешно! Перезагрузите компьютер и продолжите настройку системы.")

if __name__ == "__main__":
    setup_arch()
