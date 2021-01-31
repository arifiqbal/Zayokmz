class Config:
    def __init__(self, network, name, query, colour):
        self.network = network
        self.name = name
        self.query = query
        self.colour = colour


    def __str__(self):
        return "Network : {network} \nName :{name} \nColour :{colour} \nQuery :{query} \n------------------------------------------------".format(network = self.network, name = self.name,query = self.query,colour = self.colour,)
