from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import zipfile

app = Flask(__name__)

# Функция для распределения email
def distribute_emails(email_list, daily_plan):
    start_idx = 0
    output_files = []
    for i, count in enumerate(daily_plan):
        daily_emails = email_list[start_idx:start_idx + count]
        
        # Создаем DataFrame и добавляем заголовок 'email'
        df = pd.DataFrame(daily_emails, columns=["email"])
        
        # Имя файла
        filename = f'day_{i + 1}.csv'
        df.to_csv(filename, index=False)
        output_files.append(filename)
        
        # Увеличиваем индекс для следующей порции почт
        start_idx += count
    
    return output_files

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получение почт и плана
        emails = request.form["emails"]
        plan = request.form["plan"]

        # Преобразование введенных данных
        email_list = emails.splitlines()  # Разделение почт по строкам
        daily_plan = list(map(int, plan.splitlines()))  # Преобразование плана в список чисел

        # Распределение почт
        files = distribute_emails(email_list, daily_plan)

        # Архивация файлов и отправка пользователю
        archive_name = "email_files.zip"
        with zipfile.ZipFile(archive_name, 'w') as zipf:
            for file in files:
                zipf.write(file)
                os.remove(file)  # Удаляем файл после архивации

        return send_file(archive_name, as_attachment=True)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
