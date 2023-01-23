import subprocess
import pandas as pd
from time import strftime

with open('out.csv', 'w+') as f:
    subprocess.run('ps aux', shell=True, stdout=f)
f = open("out.csv", "r")
lines = f.readlines()
df = pd.DataFrame()

for line in lines[1:]:
    user = line.split()[0]
    process = line.split()[10]
    memory = float(line.split()[3])
    cpu = float(line.split()[2])
    dictionary = {'user': user, 'memory': memory, 'cpu': cpu, 'process': process}
    df = df._append(dictionary, ignore_index=True)

newline = '\n'
report = ('Отчёт о состоянии системы:'
          f'\nПользователи системы: {", ".join(df["user"].unique())}'
          f'\nПроцессов запущено: {df["process"].count()}'
          f'\nПользовательских процессов:'
          f'\n{newline.join(f"{col_name}: {data}" for col_name, data in df.groupby("user")["process"].count().items())}'
          f'\nВсего памяти используется: {df["memory"].sum():.1f} mb'
          f'\nВсего CPU используется: {df["cpu"].max():.1f}%'
          f'\nБольше всего памяти использует: {df.loc[df["memory"].idxmax()]["process"][:20]}'
          f'\nБольше всего CPU использует: {df.loc[df["cpu"].idxmax()]["process"][:20]}')

print(report)

datetime = strftime('%d-%m-%Y-%H:%M')
with open(f'{datetime}-scan.txt', 'w') as file:
    file.write(report)
