#!/usr/bin/env expect

# Запуск установки MongoDB
spawn apt-get install -y mongodb-org

# Ожидание запроса на ввод данных
expect "Geographic area" {
    # Отправка значения 8 для выбора нужного географического региона
    send "8\r"
}

# Ожидание следующего запроса на ввод данных
expect "Geographic area" {
    # Отправка значения 34 для выбора нужного географического региона
    send "34\r"
}

# Ожидание завершения установки
expect eof
