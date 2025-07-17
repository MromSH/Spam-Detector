import pandas as pd
import matplotlib.pyplot as plt

def create_text_report(report_path, df_path):
    df = pd.read_csv(df_path, sep="\t", header=None, names = ['label', 'message'])
    df['msg_len'] = df['message'].apply(len)
    df['word_quant'] = df['message'].apply(lambda x: len(x.split()))
    overall_quantity = len(df)
    ham_quantity = len(df[df["label"] == "ham"])
    spam_quantity = len(df[df["label"] == "spam"])
    avg_overall_len = df['msg_len'].mean()
    avg_spam_len = df[df['label'] == 'spam']['msg_len'].mean()
    avg_ham_len = df[df['label'] == 'ham']['msg_len'].mean()
    prc_ham = round((ham_quantity / overall_quantity) * 100, 2)
    prc_spam = round((spam_quantity / overall_quantity) * 100, 2)
    avg_word_quantity_overall = df['word_quant'].mean()
    avg_word_quantity_spam = df[df['label'] == 'spam']['word_quant'].mean()
    avg_word_quantity_ham = df[df['label'] == 'ham']['word_quant'].mean()

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Текстовый отчет о датасете\n\n")
        f.write("Общая информация:\n")
        f.write(f"\tОбщее количество сообщений: {overall_quantity}\n")
        f.write(f"\tСредняя длина сообщения: {avg_overall_len}\n")
        f.write(f"\tСреднее количество слов в сообщении: {avg_word_quantity_overall}\n")
        f.write(f"\tПроцентное соотношение спам-сообщений к обычным сообщениям (spam/ham): {prc_spam}% к {prc_ham}%\n\n")

        f.write("Инормация о спам-сообщениях:\n")
        f.write(f"\tКоличество спам-сообщений: {spam_quantity}\n")
        f.write(f"\tСредняя длина спам-сообщения: {avg_spam_len}\n")
        f.write(f"\tСреднее количество слов в спам-сообщении: {avg_word_quantity_spam}\n\n")

        f.write("Инормация об обычных сообщениях:\n")
        f.write(f"\tКоличество обычных сообщений: {ham_quantity}\n")
        f.write(f"\tСредняя длина обычного сообщения: {avg_ham_len}\n")
        f.write(f"\tСреднее количество слов в обычном сообщении: {avg_word_quantity_ham}")
    f.close()

def create_graphic_report(report_path, df_path):
    df = pd.read_csv(df_path, sep="\t", header=None, names = ['label', 'message'])

    plt.figure(figsize=(16, 10))
    groups = ["Не спам", "Спам"]
    counts = [len(df[df['label'] == 'ham']), len(df[df['label'] == 'spam'])]
    bars = plt.bar(groups, counts, color=['green', 'red'], label=['Не спам', 'Спам'])

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12)

    plt.title('Соотношение количества записей по группам', fontsize=14)
    plt.xlabel('Группа', fontsize=12)
    plt.ylabel('Количество записей', fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.legend(title='Легенда', loc='upper right')

    plt.savefig(report_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_model_report(conf_matrix, report, accuracy, unhandled_messages, report_path):
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Отчет по работе модели\n\n")
        f.write(f"Матрица ошибок:\n{conf_matrix}\n\n")
        f.write(f"Классификационный отчет:\n{report}\n\n")
        f.write(f"Общая точность модели: {accuracy:.4f}\n\n")
        f.write("Необработанные сообщения:\n")
        f.write(unhandled_messages)
    f.close()
