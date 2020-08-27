import os

time_list = []
del_list=[]
path = '/home/gidonyx/PycharmProjects/pythonProject/test_directory/'
files_quantity = 0
for file in os.listdir(path):
    if os.path.isfile:
        files_quantity+=1
print(files_quantity)

for file in os.listdir(path):
    time_list.append(os.path.getctime(path+file))
time_list.sort()
print(time_list)

if files_quantity > 14:

    files_del = files_quantity - 14
    i=0
    while files_del != 0:
        del_list.append(time_list[i])
        files_del -=1
        i+=1
k=0
for file in os.listdir(path):
    creation_time = os.path.getctime(path+file)
    if creation_time in del_list:
        os.remove(path+file)


