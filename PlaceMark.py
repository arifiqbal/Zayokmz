class PlaceMark:
    def __init__(self, cli_code, site, street, city, state, country, equipment, long, lat):
        self.cli_code = cli_code
        self.site = site
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.equipment = equipment
        self.long = long
        self.lat = lat
        self.comment = None

    def setComment(self, comment):
        self.comment = comment

    def setLongitude(self, long):
        self.long = long

    def setLattitude(self, lat):
        self.lat = lat

    def __str__(self):
        print(self.cli_code)
        print(self.site)
        print(self.street)
        print(self.city)
        print(self.state)
        print(self.country)
        print(self.equipment)
        print(self.long)
        print(self.lat)
        print(self.comment)
        return '---'
