import random
c = 0
for i in range(100):
        end = False
        prize = [100,50,20,10,5]
        rem = 5
        while not end:
                if random.randint(1, rem) == 1:
                        c += prize[5-rem]
                        end = True
                else:
                        rem -= 1
print(c/100)
