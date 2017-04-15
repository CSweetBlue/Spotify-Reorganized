import matplotlib.pyplot as plt
import copy


x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
y = [0, 1, 2, 3, 4, 5, 6, 8, 7]


def dictSortPeakFun2(x, y):
        """
        Function: Sorts into a Peak shape.
        Returns: (List of) New order of song keys.
        """
        
        d = dict(zip(y, x))
        yMod = sortPeakFunc(y)
        xMod = []
        
        for i in range(len(yMod)):
                xMod.append(d.get(yMod[i]))
        
        return xMod

def sortToGreatestFunc(x, y):
        """
        Function: Sorts to increasing value.
        Returns: (List of) New order of song keys.
        """
        d = dict(zip(y, x))
        yMod = list(sorted(y))
        xMod = []
        
        for i in range(len(yMod)):
                xMod.append(d.get(yMod[i]))
        
        return xMod


def sortToLeastFunc(x, y):
        """
        Function: Sorts to decreasing value.
        Returns: (List of) New order of song keys.
        """
        
        d = dict(zip(y, x))
        yMod = list(sorted(y, reverse = True))
        xMod = []
        
        for i in range(len(yMod)):
                xMod.append(d.get(yMod[i]))
        
        return xMod


#-----------------------------------------------------------------------#


def sortPeakFunc(y):
        """
        Function: Sorts into a Peak shape.
        Returns: (List of) New order of values passed in.
        """
        
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
