from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Конфигурация
BOT_TOKEN = 'твой_токен_бота'

# Тут должна быть связь user_id или email с chat_id
# Примерная таблица:
users = {
    "client123": 123456789,  # Здесь chat_id из Telegram
}

@app.route('/submit-visit', methods=['POST'])
def submit_visit():
    data = request.json
    print("Получено:", data)

    service = data.get("service")
    staff = data.get("staff")
    datetime = data.get("datetime")
    user_id = data.get("user_id")  # Ты должен передать это с фронта

    chat_id = users.get(user_id)
    if not chat_id:
        return jsonify({"error": "Пользователь не найден"}), 404

    text = f"✅ Ваша запись подтверждена:\n🛠 Услуга: {service}\n👤 Сотрудник: {staff}\n📅 Дата: {datetime}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(url, data={"chat_id": chat_id, "text": text})
    if response.ok:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"error": "Не удалось отправить сообщение"}), 500

if __name__ == '__main__':
    app.run(debug=True)
