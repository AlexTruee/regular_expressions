from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re


def merge_lists(list1, list2):
    merge_list = []
    for i in range(len(list2)):
        if list2[i] == '':
            merge_list.append(list1[i])
        else:
            merge_list.append(list2[i])
    return merge_list


def merge_contacts():
    with open("phonebook_raw.csv", encoding="utf-8-sig") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)

    # TODO 1: выполните пункты 1-3 ДЗ
    # 1 поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
    for row in contacts_list:
        fields_fio = ' '.join(row[:3]).strip().split()
        fields_fio = fields_fio + [''] * (3 - len(fields_fio))
        row[:3] = fields_fio[:3]

        # 2. Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой:
        # +7(999)999-99-99 доб.9999. Подсказка: используйте регулярки для обработки телефонов.
        result_phone = re.sub(
            r"(\+7|8)\W*(\d{3})\W*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})",
            r"+7(\2)\3-\4-\5", row[5])
        result = re.sub(r"\(*доб.\s*(\d{4})\)*", r"доб.\1", result_phone)
        row[5] = result
    # 3. Объединить все дублирующиеся записи о человеке в одну.
    # Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).
    contacts_list_new = [contacts_list[0]]
    done_index_list = []
    for index in range(1, len(contacts_list)):
        row = contacts_list[index]
        coincidence_list = [
            n for n, x in enumerate(contacts_list) if x[:2] == row[:2]
        ]
        merge_list = [''] * len(row)
        for coincidence in coincidence_list:
            if coincidence not in done_index_list:
                merge_list = merge_lists(contacts_list[coincidence], merge_list)
                done_index_list.append(coincidence)
        if ''.join(merge_list) != '':
            contacts_list_new.append(merge_list)
    #pprint(contacts_list_new)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8-sig") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list_new)


if __name__ == '__main__':
    merge_contacts()
