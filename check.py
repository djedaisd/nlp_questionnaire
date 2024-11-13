import openai

# Убедитесь, что у вас правильно установлен API ключ
openai.api_key = "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"

# Получение информации о квоте
account_info = openai.Account.retrieve()

print(account_info)
