from discord.ext import commands


class Chem(commands.Cog):
    "Chemistry utilities"

    def __init__(self, client):
        self.client = client

    @commands.command(help="Balancing the chemstry equations")
    async def balance(self, ctx, *, eq):
        eq = eq.split("=")
        import re
        from sympy import Matrix, lcm
        elementList = []
        elementMatrix = []
        try:
            reactants = eq[0]
            products = eq[1]
            reactants = reactants.replace(' ', '').split("+")
            products = products.replace(' ', '').split("+")
        except IndexError:
            await ctx.send('Please try again with the correct format, eg: Cu + HNO3 = Cu(NO3)2 + NO + H2O')
            return

        def addToMatrix(element, index, count, side):
            if(index == len(elementMatrix)):
                elementMatrix.append([])
                for x in elementList:
                    elementMatrix[index].append(0)
            if(element not in elementList):
                elementList.append(element)
                for i in range(len(elementMatrix)):
                    elementMatrix[i].append(0)
            column = elementList.index(element)
            elementMatrix[index][column] += count*side

        def findElements(segment, index, multiplier, side):
            elementsAndNumbers = re.split('([A-Z][a-z]?)', segment)
            i = 0
            while(i < len(elementsAndNumbers)-1):  # last element always blank
                i += 1
                if(len(elementsAndNumbers[i]) > 0):
                    if(elementsAndNumbers[i+1].isdigit()):
                        count = int(elementsAndNumbers[i+1])*multiplier
                        addToMatrix(elementsAndNumbers[i], index, count, side)
                        i += 1
                    else:
                        addToMatrix(
                            elementsAndNumbers[i], index, multiplier, side)

        def compoundDecipher(compound, index, side):
            segments = re.split('(\([A-Za-z0-9]*\)[0-9]*)', compound)
            for segment in segments:
                if segment.startswith("("):
                    segment = re.split('\)([0-9]*)', segment)
                    multiplier = int(segment[1])
                    segment = segment[0][1:]
                else:
                    multiplier = 1
                findElements(segment, index, multiplier, side)

        for i in range(len(reactants)):
            compoundDecipher(reactants[i], i, 1)
        for i in range(len(products)):
            compoundDecipher(products[i], i+len(reactants), -1)
        elementMatrix = Matrix(elementMatrix)
        elementMatrix = elementMatrix.transpose()
        solution = elementMatrix.nullspace()[0]
        multiple = lcm([val.q for val in solution])
        solution = multiple*solution
        coEffi = solution.tolist()
        output = ""
        for i in range(len(reactants)):
            output += str(coEffi[i][0])+reactants[i]
            if i < len(reactants)-1:
                output += " + "
        output += " → "
        for i in range(len(products)):
            output += str(coEffi[i+len(reactants)][0])+products[i]
            if i < len(products)-1:
                output += " + "
        await ctx.send(output)


def setup(client):
    client.add_cog(Chem(client))
