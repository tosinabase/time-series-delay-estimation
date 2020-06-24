import os
from subprocess import Popen, PIPE

if not os.path.exists('results'):
    os.makedirs('results')

if not os.path.exists('results/default'):
    os.makedirs('results/default')

if not os.path.exists('results/shifted'):
    os.makedirs('results/shifted')

if not os.path.exists('results/max_cor'):
    os.makedirs('results/max_cor')

number_of_threads = 12
start_num = 0
end_num = 10000

# number_of_threads - количество параллельно запущенных скриптов.
# start_num, end_num - начальный и последний номера выходных файлов.
# Общее количество получаемых файлов должно превышать число потоков.

processes = []
current_num = start_num + number_of_threads

for num in range(start_num, current_num):
    p = Popen(["venv/bin/python3", "generate_and_check.py", str(num)],
              stdout=PIPE, stderr=PIPE)
    processes.append(p)


while current_num < end_num:

    for i in range(0, number_of_threads):

        if processes[i].poll() is not None:

            # Проверка на наличие ошибок
            process_output = processes[i].communicate()
            if process_output[1] != b'':
                print('Error on {}:'.format(current_num))
                print(process_output[1].decode('utf-8'))

            # Уничтожение завершенного процесса и создание нового
            processes[i].kill()
            processes[i] = Popen(["venv/bin/python3", "generate_and_check.py", str(current_num)],
                                 stdout=PIPE, stderr=PIPE)
            current_num += 1
        else:
            ert = 'ert'

# Будем ждать завершения всех оставшихся процессов
while len(processes) != 0:
    for process in processes:
        if process.poll() is not None:
            process_output = process.communicate()

            if process_output[1] != b'':

                print('Error on {}:'.format(current_num))
                print(process_output[1].decode('utf-8'))

            processes.remove(process)
