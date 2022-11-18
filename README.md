# Arbitrum smart contracts deployer | Dev: [@python_web3](https://t.me/python_web3)
Прокачивает кошельки на сети arbitrum, путём деплоя контракта, его пополнения и вывода средств.

## Установка
1. [Скачиваем](https://www.python.org/downloads/) и устанавливаем Python.  
2. [Скачиваем](https://github.com/SomeWeb3/arbitrum_contract_deployer/archive/refs/heads/main.zip) и распаковываем проект.
3. Запускаем `install.bat`: этот файл установит отсутствующие библиотеки. Установка может занять несколько минут.

## Настройка
1. Создаём `wallets.txt` и закидываем в него приватники.
2. Создаём файл `.env` по образцу `.env.example`.\
В `ARBITRUM_URL=` надо вставить ссылку на подключение к блокчейну arbitrum. Для этого надо зарегистрироваться [здесь](https://alchemy.com/) и создать приложение в сети arbitrum mainnet. Далее нажать VIEW KEY и скопировать HTTPS.

## Запуск
1. Запускаем `start.bat`. Логи пишуться в папку `log`.
