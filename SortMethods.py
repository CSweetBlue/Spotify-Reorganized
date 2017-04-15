import matplotlib.pyplot as plt
import copy

x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y = [0, 1, 2, 3, 4, 5, 6, 8, 7]

def sortSinFunc(y):
        count = 0
        z = copy.deepcopy(y)
        z.sort()
        y1 = []
        y2 = []
        
        for i in range(len(y)):
                if count % 2:
                        y1.append(z[-1])
                else:
                        y2.append(z[-1])
                
                z.remove(z[-1])
                count+=1
        
        y2 = y2[::-1]
        y = y2 + y1
        
        return y

def sortToGreatestFunc(y):
        
        return list(sorted(y))

def sortToLeastFunc(y):

        return list(sorted(y, reverse = True))
        

yMod = sortToGreatestFunc(y)

plt.scatter(x, yMod)
