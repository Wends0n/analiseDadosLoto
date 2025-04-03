nome = input("Informe um nome")

for num in range(0,len(nome)):
    if(nome[num] == "a"):
        print("tem vogal")
    print(f"{nome[num]}")
