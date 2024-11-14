from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL da página com a matriz curricular
url = 'https://smd.ufc.br/pt/sobre-o-curso/matrizcurriculardiurno/'
response = requests.get(url)
content = response.content
soup = BeautifulSoup(content, 'html.parser')

# Localiza todas as tabelas de semestres
semester_tables = soup.findAll('tbody')
course_data = []  # Lista para armazenar todas as informações das disciplinas, incluindo pré-requisitos concatenados
last_course_entry = None  # Armazena a última entrada de disciplina completa

for semester_index in range(len(semester_tables)):
    semester_table = semester_tables[semester_index]
    course_rows = semester_table.findAll('tr')[1:]  # Ignora o cabeçalho da tabela

    for row in course_rows:
        columns = row.findAll('td')

        # Verifica se a linha atual representa um segundo pré-requisito (apenas 1 coluna preenchida)
        if len(columns) == 1 and last_course_entry:
            # Concatena o segundo pré-requisito à última string da lista `last_course_entry`
            last_course_entry[-1] += ' | ' + columns[0].text.strip()
            course_data[-1] = last_course_entry  # Atualiza o último item na lista `course_data`
            continue  # Passa para a próxima linha sem criar uma nova entrada

        course_entry = []
        semester_number = semester_index + 1

        # Ajusta o semestre para disciplinas eletivas
        if semester_number == 9:
            course_entry.append('semestre: 4 (Eletiva)')
        elif semester_number == 10:
            course_entry.append('semestre: 5 (Eletiva)')
        else:
            course_entry.append(f'semestre: {semester_number}')

        for column_index in range(len(columns)):
            cell_text = columns[column_index].text.strip()

            # Define pré-requisito ausente ou ignora linhas inválidas
            if column_index == 5 and not cell_text:
                course_entry.append('sem pré-requisito')
            elif column_index == 0 and not cell_text:
                course_entry.clear()
                break
            else:
                course_entry.append(cell_text)

        # Armazena a entrada de curso válida e atualiza `last_course_entry`
        if course_entry:
            last_course_entry = course_entry
            course_data.append(course_entry)

# Exibe todos os dados de cursos após o processamento
# for course in course_data:
#     print(course)

course_data_table = pd.DataFrame(course_data,
                                 columns=['semestre', 'código', 'disciplina', 'carga horária', 'créditos', 'natureza',
                                          'pré-requisito'])
print(course_data_table)
course_data_table.to_csv('matriz_curricular.csv', index=False)
