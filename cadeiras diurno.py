from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://smd.ufc.br/pt/sobre-o-curso/matrizcurriculardiurno/'
response = requests.get(url)
content = response.content
soup = BeautifulSoup(content, 'html.parser')

semester_tables = soup.findAll('tbody')
course_data = []
last_course_entry = None

for semester_index in range(len(semester_tables)):
    semester_table = semester_tables[semester_index]
    course_rows = semester_table.findAll('tr')[1:]

    for row in course_rows:
        columns = row.findAll('td')

        if len(columns) == 1 and last_course_entry:
            last_course_entry[-1] += ' | ' + columns[0].text.strip()
            course_data[-1] = last_course_entry
            continue

        course_entry = []
        semester_number = semester_index + 1

        if semester_number == 9:
            course_entry.append('semestre: 4 (Eletiva)')
        elif semester_number == 10:
            course_entry.append('semestre: 5 (Eletiva)')
        else:
            course_entry.append(f'semestre: {semester_number}')

        for column_index in range(len(columns)):
            cell_text = columns[column_index].text.strip()

            if column_index == 5 and not cell_text:
                course_entry.append('sem pré-requisito')
            elif column_index == 0 and not cell_text:
                course_entry.clear()
                break
            else:
                course_entry.append(cell_text)

        if course_entry:
            last_course_entry = course_entry
            course_data.append(course_entry)

# for course in course_data:
#     print(course)

course_data_table = pd.DataFrame(course_data,
                                 columns=['semestre', 'código', 'disciplina', 'carga horária', 'créditos', 'natureza',
                                          'pré-requisito'])
print(course_data_table)
course_data_table.to_csv('matriz_curricular.csv', index=False)
