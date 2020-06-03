list1 = []
with open("./relation.txt", mode='r', encoding='UTF-8') as f:
    for line in f.readlines():
        rela_array=line.strip("\n").split(",")
        if rela_array[0] not in list1:
            list1.append(rela_array[0])
        if rela_array[1] not in list1:
            list1.append(rela_array[1])

with open("./userdict2.txt", mode='w', encoding='UTF-8') as f:
    for i in list1:
        f.write(i+" nh\n")