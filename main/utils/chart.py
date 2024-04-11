import matplotlib, os
import matplotlib.pyplot as plt

from django.conf import settings 

from main.models import TelegramUser, TelegramExpense, TelegramUserIncome

from collections import defaultdict

matplotlib.use("Agg")  

def user_chart_expense(user_id):
    model_user = TelegramUser.objects.get(user_id=user_id)

    expenses = TelegramExpense.objects.filter(user=model_user)

    data = defaultdict(float)

    for expense in expenses:
        data[expense.name] += float(expense.amount)

    if data:
        name, amount = zip(*data.items())
    else:
        name, amount = [], []

    plt.bar(name, amount)
    plt.title("График финансовых расходов!")

    temp_file_path = f"{model_user.user_id}_temp.png"
    plt.savefig(temp_file_path)

    with open(temp_file_path, 'rb') as temp_file:
        model_user.chart.save(f"{model_user.user_id}.png", temp_file)
    
    plt.close()
    os.remove(temp_file_path)

    return model_user.chart.url


def user_chart_income(user_id):
    model_user = TelegramUser.objects.get(user_id=user_id)

    incomes = TelegramUserIncome.objects.filter(user=model_user)

    data = defaultdict(float)

    for income in incomes:
        data[income.name] += float(income.amount)

    if data:
        name, amount = zip(*data.items())
    else:
        name, amount = [], []

    plt.bar(name, amount)
    plt.title("График финансовых доходов!")

    temp_file_path = f"{model_user.user_id}_temp.png"
    plt.savefig(temp_file_path)

    with open(temp_file_path, "rb") as temp_file:
        model_user.chart.save(f"{model_user.user_id}.png", temp_file)

    plt.close()
    os.remove(temp_file_path)

    return model_user.chart.url