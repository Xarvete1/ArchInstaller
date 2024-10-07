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
    print("Создаем основной раздел ext4...")
    run_command(f"parted {disk} --script mkpart primary ext4 1MiB 100%")

def format_partition(disk):
    """Форматирование раздела"""
    partition = f"{disk}1"
    print(f"Форматируем раздел {partition} в ext4...")
    run_command(f"mkfs.ext4 {partition}")

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
    print("Добро пожаловать в ArchInstaller на Python!")
    
    # Шаг 1: Выбор диска
    disk = select_disk()

    # Шаг 2: Разметка диска
    partition_disk(disk)

    # Шаг 3: Форматирование раздела
    format_partition(disk)

    # Шаг 4: Монтирование раздела
    mount_partition(disk)

    # Шаг 5: Установка базовой системы
    install_base_system()

    # Шаг 6: Генерация fstab
    generate_fstab()

    print("Базовая система установлена успешно! Перезагрузите компьютер и продолжите настройку системы.")

if __name__ == "__main__":
    setup_arch()
