# v2 — Expanded EU Annex II 14-allergen taxonomy + EN/ES/CA vocabulary
# Vocabulary expanded ~2-3x over v1 to reduce lexical repetition and overfitting risk.

ALLERGENS = {
    "gluten": {
        "en": "Cereals containing gluten", "es": "Cereales que contienen gluten", "ca": "Cereals que contenen gluten",
        "code_hint": {"en": "may appear as wheat/rye/barley/oats/spelt/kamut derivatives", "es": "puede aparecer como derivados de trigo/centeno/cebada/avena/espelta/kamut", "ca": "pot aparèixer com a derivats de blat/sègol/ordi/civada/espelta/kamut"},
        "triggers": {
            "en": ["wheat flour", "wheat starch", "barley malt extract", "rye flour", "oat flakes",
                   "durum wheat semolina", "breadcrumbs (wheat)", "spelt flour", "kamut flour",
                   "wheat bran", "malted barley", "vital wheat gluten", "couscous (wheat)"],
            "es": ["harina de trigo", "almidon de trigo", "extracto de malta de cebada", "harina de centeno", "copos de avena",
                   "semola de trigo duro", "pan rallado (trigo)", "harina de espelta", "harina de kamut",
                   "salvado de trigo", "cebada malteada", "gluten de trigo vital", "cuscus (trigo)"],
            "ca": ["farina de blat", "midó de blat", "extracte de malt d'ordi", "farina de sègol", "flocs de civada",
                   "semola de blat dur", "pa ratllat (blat)", "farina d'espelta", "farina de kamut",
                   "segó de blat", "ordi maltat", "gluten de blat vital", "cuscus (blat)"],
        },
    },
    "crustaceans": {
        "en": "Crustaceans", "es": "Crustaceos", "ca": "Crustacis",
        "triggers": {
            "en": ["shrimp paste", "prawn stock", "crab extract", "langoustine bisque base",
                   "crayfish tail meat", "shrimp powder seasoning", "crab stick surimi blend"],
            "es": ["pasta de gambas", "caldo de langostinos", "extracto de cangrejo", "base de bisque de cigala",
                   "cola de cangrejo de rio", "sazonador en polvo de gamba", "mezcla de surimi de cangrejo"],
            "ca": ["pasta de gambes", "brou de llagostins", "extracte de cranc", "base de bisc de llagostí",
                   "cua de cranc de riu", "condiment en pols de gamba", "barreja de surimi de cranc"],
        },
    },
    "eggs": {
        "en": "Eggs", "es": "Huevos", "ca": "Ous",
        "triggers": {
            "en": ["pasteurized egg yolk", "whole egg powder", "egg white (albumen)", "liquid whole egg",
                   "egg lecithin", "mayonnaise (contains egg)", "egg wash glaze"],
            "es": ["yema de huevo pasteurizada", "huevo entero en polvo", "clara de huevo (albumina)", "huevo liquido entero",
                   "lecitina de huevo", "mayonesa (contiene huevo)", "glaseado de huevo batido"],
            "ca": ["rovell d'ou pasteuritzat", "ou sencer en pols", "clara d'ou (albumina)", "ou líquid sencer",
                   "lecitina d'ou", "maionesa (conté ou)", "vernís d'ou batut"],
        },
    },
    "fish": {
        "en": "Fish", "es": "Pescado", "ca": "Peix",
        "triggers": {
            "en": ["anchovy fillet", "fish sauce", "bonito flakes", "cod stock", "worcestershire sauce (contains fish)",
                   "fish gelatin", "tuna extract", "sardine oil"],
            "es": ["filete de anchoa", "salsa de pescado", "copos de bonito", "caldo de bacalao", "salsa worcestershire (contiene pescado)",
                   "gelatina de pescado", "extracto de atun", "aceite de sardina"],
            "ca": ["filet d'anxova", "salsa de peix", "flocs de bonítol", "brou de bacallà", "salsa worcestershire (conté peix)",
                   "gelatina de peix", "extracte de tonyina", "oli de sardina"],
        },
    },
    "peanuts": {
        "en": "Peanuts", "es": "Cacahuetes", "ca": "Cacauets",
        "triggers": {
            "en": ["peanut oil", "peanut butter", "roasted peanuts", "peanut flour", "satay sauce (peanut base)", "peanut brittle pieces"],
            "es": ["aceite de cacahuete", "mantequilla de cacahuete", "cacahuetes tostados", "harina de cacahuete", "salsa satay (base de cacahuete)", "trozos de crocante de cacahuete"],
            "ca": ["oli de cacauet", "mantega de cacauet", "cacauets torrats", "farina de cacauet", "salsa satay (base de cacauet)", "trossos de crocant de cacauet"],
        },
    },
    "soy": {
        "en": "Soybeans", "es": "Soja", "ca": "Soia",
        "triggers": {
            "en": ["soy lecithin", "soy sauce", "textured soy protein", "soybean oil", "tofu cubes", "miso paste (soy)", "edamame puree"],
            "es": ["lecitina de soja", "salsa de soja", "proteina de soja texturizada", "aceite de soja", "cubos de tofu", "pasta de miso (soja)", "pure de edamame"],
            "ca": ["lecitina de soia", "salsa de soia", "proteïna de soia texturitzada", "oli de soia", "cubs de tofu", "pasta de miso (soia)", "puré d'edamame"],
        },
    },
    "milk": {
        "en": "Milk (including lactose)", "es": "Leche (incluida la lactosa)", "ca": "Llet (inclosa la lactosa)",
        "triggers": {
            "en": ["whole milk powder", "butter", "cream", "whey powder", "parmesan cheese", "lactose",
                   "condensed milk", "buttermilk", "casein", "mozzarella cheese", "ghee"],
            "es": ["leche entera en polvo", "mantequilla", "nata", "suero de leche en polvo", "queso parmesano", "lactosa",
                   "leche condensada", "suero de mantequilla", "caseina", "queso mozzarella", "ghee"],
            "ca": ["llet sencera en pols", "mantega", "nata", "sèrum de llet en pols", "formatge parmesà", "lactosa",
                   "llet condensada", "sèrum de mantega", "caseïna", "formatge mozzarella", "ghee"],
        },
    },
    "nuts": {
        "en": "Tree nuts", "es": "Frutos de cascara", "ca": "Fruits de closca",
        "triggers": {
            "en": ["almond flour", "hazelnut paste", "walnut pieces", "cashew butter", "pistachio paste",
                   "pine nuts", "macadamia crumble", "brazil nut pieces", "pecan halves"],
            "es": ["harina de almendra", "pasta de avellana", "trozos de nuez", "mantequilla de anacardo", "pasta de pistacho",
                   "pinones", "crumble de macadamia", "trozos de nuez de brasil", "mitades de pecana"],
            "ca": ["farina d'ametlla", "pasta d'avellana", "trossos de nou", "mantega d'anacard", "pasta de pistatxo",
                   "pinyons", "crumble de macadàmia", "trossos de nou del brasil", "meitats de pacana"],
        },
    },
    "celery": {
        "en": "Celery", "es": "Apio", "ca": "Api",
        "triggers": {
            "en": ["celery salt", "celeriac puree", "dried celery", "celery seed extract", "celery stock cube"],
            "es": ["sal de apio", "pure de apio nabo", "apio deshidratado", "extracto de semilla de apio", "pastilla de caldo de apio"],
            "ca": ["sal d'api", "puré d'api rave", "api deshidratat", "extracte de llavor d'api", "pastilla de brou d'api"],
        },
    },
    "mustard": {
        "en": "Mustard", "es": "Mostaza", "ca": "Mostassa",
        "triggers": {
            "en": ["mustard seed", "dijon mustard", "mustard powder", "wholegrain mustard", "mustard oil"],
            "es": ["semilla de mostaza", "mostaza de dijon", "mostaza en polvo", "mostaza en grano", "aceite de mostaza"],
            "ca": ["llavor de mostassa", "mostassa de dijon", "mostassa en pols", "mostassa en gra", "oli de mostassa"],
        },
    },
    "sesame": {
        "en": "Sesame seeds", "es": "Semillas de sesamo", "ca": "Llavors de sèsam",
        "triggers": {
            "en": ["tahini", "sesame oil", "toasted sesame seeds", "sesame paste", "black sesame garnish"],
            "es": ["tahini", "aceite de sesamo", "semillas de sesamo tostadas", "pasta de sesamo", "guarnicion de sesamo negro"],
            "ca": ["tahini", "oli de sèsam", "llavors de sèsam torrades", "pasta de sèsam", "guarniment de sèsam negre"],
        },
    },
    "sulphites": {
        "en": "Sulphur dioxide and sulphites (>10mg/kg)", "es": "Dioxido de azufre y sulfitos (>10mg/kg)", "ca": "Diòxid de sofre i sulfits (>10mg/kg)",
        "triggers": {
            "en": ["sulphur dioxide (preservative E220)", "sodium metabisulphite (E223)", "dried apricots (sulphited)",
                   "potassium bisulphite (E228)", "white wine vinegar (sulphite-treated)"],
            "es": ["dioxido de azufre (conservante E220)", "metabisulfito sodico (E223)", "orejones de albaricoque (sulfitados)",
                   "bisulfito potasico (E228)", "vinagre de vino blanco (tratado con sulfitos)"],
            "ca": ["diòxid de sofre (conservant E220)", "metabisulfit sòdic (E223)", "orellanes d'albercoc (sulfitades)",
                   "bisulfit potàssic (E228)", "vinagre de vi blanc (tractat amb sulfits)"],
        },
    },
    "lupin": {
        "en": "Lupin", "es": "Altramuces", "ca": "Tramussos",
        "triggers": {
            "en": ["lupin flour", "lupin seeds", "lupin protein isolate"],
            "es": ["harina de altramuz", "semillas de altramuz", "aislado de proteina de altramuz"],
            "ca": ["farina de tramús", "llavors de tramús", "aïllat de proteïna de tramús"],
        },
    },
    "molluscs": {
        "en": "Molluscs", "es": "Moluscos", "ca": "Mol·luscs",
        "triggers": {
            "en": ["mussel meat", "squid rings", "oyster sauce", "clam broth", "octopus pieces"],
            "es": ["carne de mejillon", "aros de calamar", "salsa de ostras", "caldo de almejas", "trozos de pulpo"],
            "ca": ["carn de musclo", "anelles de calamar", "salsa d'ostres", "brou de cloïsses", "trossos de pop"],
        },
    },
}

NEUTRAL_INGREDIENTS = {
    "en": ["water", "salt", "sunflower oil", "sugar", "onion powder", "black pepper", "paprika",
           "tomato concentrate", "citric acid", "potato starch", "rice flour", "olive oil",
           "garlic powder", "yeast extract", "carrot", "vinegar", "bay leaf", "rosemary",
           "corn starch", "cane sugar", "leek", "thyme", "oregano", "smoked paprika", "brown sugar",
           "canola oil", "vegetable stock powder", "dried parsley", "cumin", "turmeric",
           "coriander seed", "chili flakes", "white pepper", "shallot", "ginger powder",
           "lemon zest", "apple cider vinegar", "modified corn starch", "maltodextrin", "xanthan gum"],
    "es": ["agua", "sal", "aceite de girasol", "azucar", "cebolla en polvo", "pimienta negra", "pimenton",
           "concentrado de tomate", "acido citrico", "almidon de patata", "harina de arroz", "aceite de oliva",
           "ajo en polvo", "extracto de levadura", "zanahoria", "vinagre", "hoja de laurel", "romero",
           "almidon de maiz", "azucar de cana", "puerro", "tomillo", "oregano", "pimenton ahumado", "azucar moreno",
           "aceite de colza", "caldo vegetal en polvo", "perejil deshidratado", "comino", "curcuma",
           "semilla de cilantro", "copos de chile", "pimienta blanca", "chalota", "jengibre en polvo",
           "ralladura de limon", "vinagre de sidra de manzana", "almidon de maiz modificado", "maltodextrina", "goma xantana"],
    "ca": ["aigua", "sal", "oli de gira-sol", "sucre", "ceba en pols", "pebre negre", "pebre vermell",
           "concentrat de tomàquet", "àcid cítric", "midó de patata", "farina d'arròs", "oli d'oliva",
           "all en pols", "extracte de llevat", "pastanaga", "vinagre", "fulla de llorer", "romaní",
           "midó de blat de moro", "sucre de canya", "porro", "farigola", "orenga", "pebre vermell fumat", "sucre moré",
           "oli de colza", "brou vegetal en pols", "julivert deshidratat", "comí", "curcuma",
           "llavor de coriandre", "flocs de xili", "pebre blanc", "escalunya", "gingebre en pols",
           "ratlladura de llimona", "vinagre de sidra de poma", "midó de blat de moro modificat", "maltodextrina", "goma xantana"],
}

PRODUCT_NAMES = {
    "en": ["Béchamel Sauce Base", "Frozen Croquettes Mix", "Bread Roll Dough", "Chicken Broth Concentrate",
           "Chocolate Mousse Powder", "Marinara Sauce", "Battered Calamari", "Vegetable Stock Cube",
           "Puff Pastry Sheets", "Salad Dressing Vinaigrette", "Meatball Mix", "Tomato Soup Base",
           "Frozen Fish Fingers", "Seafood Paella Base", "Custard Powder", "Gazpacho Concentrate",
           "Pizza Dough Ball", "Aioli Sauce", "Romesco Sauce Base", "Empanada Filling Mix",
           "Croissant Dough", "Ratatouille Mix", "Beef Stock Paste", "Panna Cotta Powder",
           "Hummus Base"],
    "es": ["Base de Salsa Bechamel", "Mezcla de Croquetas Congeladas", "Masa de Pan de Bollo", "Concentrado de Caldo de Pollo",
           "Polvo de Mousse de Chocolate", "Salsa Marinara", "Calamares Rebozados", "Pastilla de Caldo de Verduras",
           "Laminas de Hojaldre", "Vinagreta para Ensalada", "Mezcla para Albondigas", "Base de Sopa de Tomate",
           "Palitos de Pescado Congelados", "Base para Paella de Marisco", "Polvo para Natillas", "Concentrado de Gazpacho",
           "Bola de Masa para Pizza", "Salsa Alioli", "Base de Salsa Romesco", "Relleno para Empanadas",
           "Masa de Croissant", "Mezcla para Pisto", "Pasta de Caldo de Ternera", "Polvo para Panna Cotta",
           "Base de Hummus"],
    "ca": ["Base de Salsa Beixamel", "Barreja de Croquetes Congelades", "Massa de Pa de Rosca", "Concentrat de Brou de Pollastre",
           "Pols de Mousse de Xocolata", "Salsa Marinara", "Calamars Arrebossats", "Pastilla de Brou de Verdures",
           "Làmines de Pasta de Full", "Vinagreta per a Amanida", "Barreja per a Mandonguilles", "Base de Sopa de Tomàquet",
           "Bastonets de Peix Congelats", "Base per a Paella de Marisc", "Pols per a Natilles", "Concentrat de Gaspatxo",
           "Bola de Massa per a Pizza", "Salsa Allioli", "Base de Salsa Romesco", "Farciment per a Empanades",
           "Massa de Croissant", "Barreja per a Samfaina", "Pasta de Brou de Vedella", "Pols per a Panna Cotta",
           "Base d'Hummus"],
}

SUPPLIER_NAMES = [
    "Distribuciones Alimentarias Mediterraneo S.L.", "Congelados del Ebro S.A.", "Ibérica Food Supply Co.",
    "Proveedora Catalana de Alimentacion", "Grup Alimentari Barcelona S.L.", "Nordic Frozen Foods AB",
    "Delta Gourmet Ingredients", "Sabor & Origen Distribucion S.L.", "EuroFood Wholesale B.V.",
    "Cocina Central Suministros S.A.", "Mercat Central Distribucio S.L.", "Levante Alimentacion Mayorista S.A.",
    "Costa Brava Foodservice S.L.", "Andalusian Fine Foods Export S.L.", "Basque Coast Seafood Supply S.L.",
    "Girona Gastro Ingredients S.C.P.", "Valencia Wholesale Foods S.A.", "Nortena Distribucion Alimentaria S.L.",
    "Balear Food Import-Export S.L.", "Provenza Delicatessen Import S.A.", "Aragon Central Kitchen Supply S.L.",
    "Roma Fine Foods Trading S.r.l.", "Lyon Gastronomie Distribution SARL", "Porto Foodservice Import Lda.",
    "Milano Ingredienti Premium S.p.A.",
]

COUNTRIES_OF_ORIGIN = {
    "en": ["Spain", "France", "Italy", "Portugal", "Netherlands", "Germany", "Morocco", "Belgium"],
    "es": ["Espana", "Francia", "Italia", "Portugal", "Paises Bajos", "Alemania", "Marruecos", "Belgica"],
    "ca": ["Espanya", "Franca", "Italia", "Portugal", "Paisos Baixos", "Alemanya", "Marroc", "Belgica"],
}

STORAGE_CONDITIONS = {
    "en": ["Store at 0-4C, keep refrigerated", "Store frozen at -18C or below", "Store in a cool, dry place below 25C",
           "Keep refrigerated after opening, consume within 3 days"],
    "es": ["Conservar entre 0-4C, mantener refrigerado", "Conservar congelado a -18C o inferior", "Conservar en lugar fresco y seco, por debajo de 25C",
           "Mantener refrigerado tras apertura, consumir en 3 dias"],
    "ca": ["Conservar entre 0-4C, mantenir refrigerat", "Conservar congelat a -18C o inferior", "Conservar en lloc fresc i sec, per sota de 25C",
           "Mantenir refrigerat despres d'obrir, consumir en 3 dies"],
}

CITY_ADDRESSES = [
    "Pol. Ind. Can Bernades, Nau 12, 08130 Santa Perpetua de Mogoda, Barcelona",
    "C/ Mercabarna, Modul B-24, 08040 Barcelona",
    "Ctra. Nacional 340 km 12, 43870 Amposta, Tarragona",
    "Pol. Ind. Fonollar, C/ Ferrers 8, 17800 Olot, Girona",
    "Av. del Puerto 45, 46023 Valencia",
    "Zona Franca, Sector C, 08040 Barcelona",
    "Poligono Malpica, Calle D 22, 50016 Zaragoza",
    "Rua do Comercio 88, 4450-208 Matosinhos, Porto",
]

LABELS_TEXT = {
    "en": {
        "spec_sheet": "PRODUCT SPECIFICATION SHEET", "product": "Product name", "supplier": "Supplier",
        "code": "Product code", "date": "Issue date", "ingredients": "Ingredients",
        "allergen_section": "ALLERGEN INFORMATION", "contains": "Contains", "may_contain": "May contain traces of",
        "free_from": "Free from", "none_declared": "No allergens declared", "matrix_title": "Allergen Matrix",
        "matrix_note": "X = present   T = may contain traces   - = not present",
        "batch": "Batch/Lot no.", "origin": "Country of origin", "storage": "Storage conditions",
        "address": "Supplier address", "net_weight": "Net weight",
    },
    "es": {
        "spec_sheet": "FICHA TECNICA DE PRODUCTO", "product": "Nombre del producto", "supplier": "Proveedor",
        "code": "Codigo de producto", "date": "Fecha de emision", "ingredients": "Ingredientes",
        "allergen_section": "INFORMACION SOBRE ALERGENOS", "contains": "Contiene", "may_contain": "Puede contener trazas de",
        "free_from": "Libre de", "none_declared": "No se declaran alergenos", "matrix_title": "Matriz de Alergenos",
        "matrix_note": "X = presente   T = puede contener trazas   - = no presente",
        "batch": "Num. de lote", "origin": "Pais de origen", "storage": "Condiciones de conservacion",
        "address": "Direccion del proveedor", "net_weight": "Peso neto",
    },
    "ca": {
        "spec_sheet": "FITXA TECNICA DE PRODUCTE", "product": "Nom del producte", "supplier": "Proveidor",
        "code": "Codi de producte", "date": "Data d'emissio", "ingredients": "Ingredients",
        "allergen_section": "INFORMACIO SOBRE AL·LERGENS", "contains": "Conte", "may_contain": "Pot contenir traces de",
        "free_from": "Lliure de", "none_declared": "No es declaren al·lergens", "matrix_title": "Matriu d'Al·lergens",
        "matrix_note": "X = present   T = pot contenir traces   - = no present",
        "batch": "Num. de lot", "origin": "Pais d'origen", "storage": "Condicions de conservacio",
        "address": "Adreca del proveidor", "net_weight": "Pes net",
    },
}
