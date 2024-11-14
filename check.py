import openai

# Убедитесь, что у вас правильно установлен API ключ
openai.api_key = ""

# Получение информации о квоте
account_info = openai.Account.retrieve()

print(account_info)
