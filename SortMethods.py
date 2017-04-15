import matplotlib.pyplot as plt
import copy


x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
y = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def sortPeakSupport(attrValues):
        """
        Function: Sorts into a Peak shape.
        Returns: (List of) New order of values passed in.
        """
        
        count = 0
        z = copy.deepcopy(attrValues)
        z.sort()
        attrValuesHalf1 = []
        attrValuesHalf2 = []
        
        for i in range(len(z)):
                if count % 2:
                        attrValuesHalf1.append(z[-1])
                else:
                        attrValuesHalf2.append(z[-1])
                
                z.remove(z[-1])
                count+=1
        
        attrValuesHalf2 = attrValuesHalf2[::-1]
        z = attrValuesHalf2 + attrValuesHalf1
        
        return z


#-----------------------------------------------------------------------#


def sortPeakFunc(songIDs, attrValues):
        """
        Function: Sorts into a Peak shape.
        Returns: (List of) New order of song keys.
        """
        
        d = dict(zip(attrValues, songIDs))
        attrValuesMod = sortPeakSupport(attrValues)
        songIDsMod = []
        
        for i in range(len(attrValuesMod)):
                songIDsMod.append(d.get(attrValuesMod[i]))
        
        print(str(attrValuesMod))
        print(str(songIDsMod))
        return songIDsMod

def sortToGreatestFunc(songIDs, attrValues):
        """
        Function: Sorts to increasing value.
        Returns: (List of) New order of song keys.
        """
        d = dict(zip(attrValues, songIDs))
        attrValuesMod = list(sorted(attrValues))
        songIDsMod = []
        
        for i in range(len(attrValuesMod)):
                songIDsMod.append(d.get(attrValuesMod[i]))
        
        print(str(attrValuesMod))
        print(str(songIDsMod))
        return songIDsMod


def sortToLeastFunc(songIDs, attrValues):
        """
        Function: Sorts to decreasing value.
        Returns: (List of) New order of song keys.
        """
        
        d = dict(zip(attrValues, songIDs))
        attrValuesMod = list(sorted(attrValues, reverse = True))
        songIDsMod = []
        
        for i in range(len(attrValuesMod)):
                songIDsMod.append(d.get(attrValuesMod[i]))
        
        print(str(attrValuesMod))
        print(str(songIDsMod))
        return songIDsMod

sortToGreatestFunc(x, y)
sortToLeastFunc(x, y)
sortPeakFunc(x, y)
