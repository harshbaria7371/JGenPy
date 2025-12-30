# data_generator/static_data.py
"""
Static data sets for data generation.
Contains predefined lists of values that can be used with the static_data generator.
"""

# Vehicle Brands
VEHICLE_BRANDS = [
    "Toyota", "Volkswagen", "Ford", "Mercedes-Benz", "BMW", "Audi",
    "Honda", "Nissan", "Peugeot", "Renault", "Citroën", "Alfa Romeo", "Chevrolet",
    "Chrysler", "Daewoo", "Ferrari", "Fiat", "Hyundai", "Isuzu", "Jaguar",
    "Jeep", "Kia", "Lamborghini", "Lancia Italia", "Land Rover", "Lexus", "Maserati",
    "Mazda", "McLaren", "Mini", "Mitsubishi", "Opel",
    "Dacia", "Saab", "Skoda", "Suzuki", "Volvo", "Seat",
    "Subaru", "Alpine", "Iveco", "Stellantis", "Tesla", "Vauxhall", "MG", "BYD",
    "Lynk & Co", "Smart", "Ssangyong"
]

# Model names by brand
MODEL_NAMES = {
    'Toyota': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Prius', 'Avalon'],
    'Volkswagen': ['Golf', 'Passat', 'Jetta', 'Tiguan', 'Atlas', 'Arteon'],
    'Ford': ['F-150', 'Mustang', 'Explorer', 'Escape', 'Focus', 'Edge'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'A-Class'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series', 'X1'],
    'Audi': ['A4', 'A6', 'Q5', 'Q7', 'A3', 'Q3'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey', 'HR-V'],
    'Nissan': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Maxima', 'Murano'],
    'Peugeot': ['208', '308', '3008', '5008', '508', '2008'],
    'Renault': ['Clio', 'Megane', 'Captur', 'Kadjar', 'Talisman', 'Scenic'],
    'Citroën': ['C3', 'C4', 'C5', 'Berlingo', 'Cactus', 'Spacetourer'],
    'Alfa Romeo': ['Giulia', 'Stelvio', 'Tonale', 'Giulietta', 'MiTo', '4C'],
    'Chevrolet': ['Camaro', 'Corvette', 'Equinox', 'Traverse', 'Silverado', 'Tahoe'],
    'Chrysler': ['300', 'Pacifica', 'Town & Country', 'Voyager', 'Sebring', 'Voyager'],
    'Daewoo': ['Nubira', 'Lacetti', 'Nexia', 'Matiz', 'Lanos', 'Nubira'],
    'Ferrari': ['488', 'F8 Tributo', 'Portofino', 'SF90 Stradale', 'SF2000', '812 Competizione'],
    'Fiat': ['500', 'Panda', 'Punto', 'Tipo', '500L', '500X'],
    'Hyundai': ['Elantra', 'Tucson', 'Santa Fe', 'Kona', 'Palisade', 'Sonata'],
    'Isuzu': ['D-Max', 'MU-X', 'Rodeo', 'Trooper', 'Trooper Sport', 'I-Series'],
    'Jaguar': ['F-Type', 'XE', 'XF', 'XJ', 'XK', 'E-Pace'],
    'Jeep': ['Wrangler', 'Cherokee', 'Grand Cherokee', 'Renegade', 'Compass', 'Gladiator'],
    'Kia': ['Sportage', 'Sorento', 'Telluride', 'Soul', 'K5', 'Stinger'],
    'Lamborghini': ['Huracan', 'Aventador', 'Urus', 'Countach', 'Centenario', 'Sian'],
    'Lancia Italia': ['Ypsilon', 'Delta', 'Punto', 'Stilo', 'Thema', 'Kappa'],
    'Land Rover': ['Defender', 'Range Rover', 'Range Rover Sport', 'Range Rover Velar', 'Discovery', 'Discovery Sport'],
    'Lexus': ['RX', 'ES', 'NX', 'LS', 'GX', 'UX'],
    'Maserati': ['Ghibli', 'Levante', 'Quattroporte', 'MC20', 'GranTurismo', 'GranCabrio'],
    'Mazda': ['CX-5', 'CX-9', 'MX-5', 'RX-8', 'CX-3', 'CX-30'],
    'Meclaren': ['720S', '765LT', '720S Spider', '720S Spider', '720S Spider', '720S Spider'],
    'Mini': ['Cooper', 'Countryman', 'Clubman', 'Paceman', 'Clubvan', 'Cabrio'],
    'Mitsubishi': ['Lancer', 'Outlander', 'ASX', 'Eclipse Cross', 'Mirage', 'Eclipse'],
    'Opel': ['Astra', 'Corsa', 'Insignia', 'Zafira', 'Meriva', 'Combo'],
    'Dacia': ['Duster', 'Sandero', 'Logan', 'Dokker', 'Dokker', 'Dokker'],
    'Saab': ['9-3', '9-5', '9-7X', '9-3 Convertible', '9-5 Convertible', '9-7X Convertible'],
    'Skoda': ['Octavia', 'Superb', 'Kodiaq', 'Karoq', 'Kamiq', 'Fabia'],
    'Suzuki': ['Swift', 'Vitara', 'Jimny', 'Baleno', 'Ignis', 'S-Cross'],
    'Volvo': ['XC40', 'XC60', 'XC90', 'S60', 'S90', 'V60'],
    'Seat': ['Ibiza', 'Leon', 'Ateca', 'Arona', 'Tarraco', 'Alhambra'],
    'Subaru': ['Forester', 'Outback', 'Impreza', 'Legacy', 'Tribeca', 'Impreza WRX'],
    'Alpine': ['A110', 'A110S', 'A110S E-Tense', 'A110S E-Tense', 'A110S E-Tense', 'A110S E-Tense'],
    'Iveco': ['Daily', 'Eurocargo', 'Stralis', 'Stralis NP', 'Stralis NP 4x4', 'Stralis NP 4x4'],
    'Stellantis': ['3008', '3008 E-Tense', '3008 E-Tense', '3008 E-Tense', '3008 E-Tense', '3008 E-Tense'],
    'Tesla': ['Model 3', 'Model Y', 'Model X', 'Model S', 'Model 3', 'Model Y'],
    'Vauxhall': ['Astra', 'Corsa', 'Insignia', 'Zafira', 'Meriva', 'Combo'],
    'MG': ['ZS', 'HS', 'ZS EV', 'HS EV', 'ZS EV', 'HS EV'],
    'Byd': ['e6', 'e9', 'e100', 'e100 Plus', 'e100 Plus', 'e100 Plus'],
    'Lynk & Co': ['01', '02', '03', '04', '05', '06'],
    'Smart': ['EQ Fortwo', 'EQ Forfour', 'EQ Forfour', 'EQ Forfour', 'EQ Forfour', 'EQ Forfour'],
    'Ssangyong': ['Tivoli', 'Korando', 'Rexton', 'Musso', 'Korando', 'Korando'],
}

# Vehicle Types
VEHICLE_TYPES = [
    "Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Wagon",
    "Pickup Truck", "Van", "Minivan", "Crossover", "Sports Car"
]

# Vehicle categories
VEHICLE_CATEGORIES = [
    'Economy', 'Compact', 'Mid-size', 'Full-size', 'Luxury',
    'Sports', 'Off-road', 'Commercial', 'Electric'
]

# Vehicle Colors
VEHICLE_COLORS = [
    "White", "Black", "Silver", "Gray", "Red", "Blue", "Green",
    "Brown", "Beige", "Gold", "Orange", "Yellow", "Purple", "Pink"
]

# Fuel Types
FUEL_TYPES = [
    'Petrol', 'Diesel', 'Hybrid', 'Electric', 'Plug-in Hybrid', 'Hydrogen'
]

# Bodywork types
BODYWORK_TYPES = [
    'Sedan', 'Hatchback', 'SUV', 'Coupe', 'Convertible', 'Wagon',
    'Pickup Truck', 'Van', 'Minivan', 'Crossover', 'Sports Car',
    'Estate', 'MPV', 'Limousine', 'Roadster', 'Targa'
]

# Dictionary mapping data set names to their lists
# This allows easy lookup by name
STATIC_DATA_SETS = {
    "vehicle_brands": VEHICLE_BRANDS,
    "vehicle_types": VEHICLE_TYPES,
    "vehicle_categories": VEHICLE_CATEGORIES,
    "vehicle_colors": VEHICLE_COLORS,
    "fuel_types": FUEL_TYPES,
    "bodywork_types": BODYWORK_TYPES,
    "model_names": MODEL_NAMES,  # Dictionary: brand -> list of models
}

