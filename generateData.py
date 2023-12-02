class ElementType:
    # an abstract representation of the water
    def __init__(self, type):
        self.type = type

class Vial:
    def __init__(self, contents, generationMode = True):
        '''
            The internal representation of a vial is a list with 4 elements, which are initialized as None
            and can be filled with a content (eg water of a particular color) from left to right.
            Provide generationMode = False if you want vial to act as it should in the game (ie can't
            pour different colors on top of one another)
        '''
        self.contents = [None, None, None, None]
        self.generationMode = generationMode
        for i in range(0, len(contents)):
            self.contents[i] = contents[i]

    def isContentPourable(self, newContent, contentIndex):
        '''
            Check if a potential new content may be poured on top of existing content
        '''
        numberOfEmptySpots = sum(x is None for x in self.contents)
        if numberOfEmptySpots == len(self.contents) or self.generationMode:
            return True
        elif self.contents[contentIndex - 1].type == newContent.type:
            return True
        else:
            return False

    def pourIn(self, newContent):
        '''
            Attempt to pour a new content in the new vial.
            Returns whether the pour was successful
        '''
        if None in self.contents:
            contentIndex = self.contents.index(None)
            if self.isContentPourable(newContent, contentIndex):
                self.contents[contentIndex] = newContent
                return True
        return False
    
    def pourOut(self):
        '''
            Returns the content that was poured out or None if empty
        '''
        if None in self.contents:
            indexOfEmpty = self.contents.index(None)
            if indexOfEmpty == 0:
                return None
            else:
                contentIndex = indexOfEmpty - 1
        else:
            contentIndex = len(self.contents) - 1
        pouredOut = self.contents[contentIndex]
        self.contents[contentIndex] = None
        return pouredOut
    
    def isEmpty(self):
        return self.contents.count(None) == len(self.contents)
    
    def hasSpace(self):
        return self.contents.count(None) != 0
    
    def getCountOfEmptySpaces(self):
        return self.contents.count(None)
    
    def __str__(self):
        output = ""
        for item in self.contents:
            if item == None:
                output += "_"
            else:
                output += item.type
        return output



class DataGenerator:
    '''
        Generates data for running experiments by taking in a number of Vials and an array of colors,
        and then shuffling them around for a certain number of steps, randomly.
        Shuffling is done in such a way to be reversable (to make sure the problem is solvable)
    '''
    def __init__(self, colors, numVials):
        self.vials = []
        self.numberOfEmpty = numVials - len(colors)
        # generates the full vials
        for i in range(len(colors)):
            currentColor = colors[i]
            self.vials.append(Vial([currentColor] * 4))
        
        # empty vials
        emptyVials = numVials - len(colors)
        for i in range(emptyVials):
            self.vials.append(Vial([]))

    def makeMove(self, vialIndex):
        '''
            Make a move; returns whether a successful move was able to be made
        '''
        indices = [i for i in range(len(self.vials))]
        random.shuffle(indices)
        for index in indices:
            if index != vialIndex:
                if self.vials[index].hasSpace():
                    self.pourFromOneIntoOther(vialIndex, index)
                    return True
        return False
    
    def pourFromOneIntoOther(self, senderVialIndex, receiverVialIndex):
        senderVial = self.vials[senderVialIndex]
        senderVialContents = senderVial.pourOut()
        receiverVial = self.vials[receiverVialIndex]
        receiverVial.pourIn(senderVialContents)
    
    def ensureEmpty(self):
        # get emptiest vial index
        emptiedVials = []
        for j in range(self.numberOfEmpty):
            emptyCount = None
            emptiestVial = None

            for i in range(len(self.vials)):
                if i not in emptiedVials:
                    vial = self.vials[i]
                    count = vial.getCountOfEmptySpaces()
                    if emptiestVial == None or emptyCount < count:
                        emptiestVial = i
                        emptyCount = count
            emptiedVials.append(emptiestVial)

            while not self.vials[emptiestVial].isEmpty():
                for i in range(len(self.vials)):
                    if i != emptiestVial and i not in emptiedVials and self.vials[i].hasSpace():
                        self.pourFromOneIntoOther(emptiestVial, i)


    def generate(self, amountOfShuffling = 150):
        for i in range(amountOfShuffling):
            vialIndex = random.randrange(len(self.vials))
            self.makeMove(vialIndex)
        self.ensureEmpty()


    def print(self):
        for vial in self.vials:
            print(vial)

import random
random.seed()

# try generating
types = [ElementType("*"), ElementType("#"), ElementType("%"), ElementType("^"), ElementType("&"), ElementType("@"), ElementType("[")]
numEmpty = 2
dataGenerator = DataGenerator(types, len(types) + numEmpty)
dataGenerator.generate()
dataGenerator.print()