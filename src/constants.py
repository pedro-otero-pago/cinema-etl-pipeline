"""
Known-value catalogs used by parser.py to classify the variable-position
fields inside the "data" block of each movie card (country, genre).

Comparisons should be done in lowercase (see parser.py), so these sets
are stored in lowercase already to avoid mismatched casing.
"""

KNOWN_COUNTRIES = {
    "afganistán", "albania", "alemania", "andorra", "angola",
    "antigua y barbuda", "arabia saudí", "argelia", "argentina", "armenia",
    "australia", "austria", "azerbaiyán", "bahamas", "bangladés",
    "barbados", "baréin", "bélgica", "belice", "benín", "bielorrusia",
    "birmania", "bolivia", "bosnia y herzegovina", "botsuana", "brasil",
    "brunéi", "bulgaria", "burkina faso", "burundi", "bután", "cabo verde",
    "camboya", "camerún", "canadá", "catar", "chad", "chile", "china",
    "chipre", "colombia", "comoras", "corea del norte", "corea del sur",
    "costa de marfil", "costa rica", "croacia", "cuba", "dinamarca",
    "dominica", "ecuador", "egipto", "el salvador", "emiratos árabes unidos",
    "ee.uu.", "estados unidos", "eritrea", "eslovaquia", "eslovenia",
    "españa", "estonia", "esuatini", "etiopía", "filipinas", "finlandia",
    "fiyi", "francia", "gabón", "gambia", "georgia", "ghana", "granada",
    "grecia", "guatemala", "guyana", "guinea", "guinea-bisáu",
    "guinea ecuatorial", "haití", "honduras", "hungría", "india",
    "indonesia", "irak", "irán", "irlanda", "islandia", "islas marshall",
    "islas salomón", "israel", "italia", "jamaica", "japón", "jordania",
    "kazajistán", "kenia", "kirguistán", "kiribati", "kuwait", "laos",
    "lesoto", "letonia", "líbano", "liberia", "libia", "liechtenstein",
    "lituania", "luxemburgo", "macedonia del norte", "madagascar",
    "malasia", "malaui", "maldivas", "malí", "malta", "marruecos",
    "mauricio", "mauritania", "méxico", "micronesia", "moldavia", "mónaco",
    "mongolia", "montenegro", "mozambique", "namibia", "nauru", "nepal",
    "nicaragua", "níger", "nigeria", "noruega", "nueva zelanda", "omán",
    "países bajos", "holanda", "pakistán", "palaos", "panamá",
    "papúa nueva guinea", "paraguay", "perú", "polonia", "portugal",
    "reino unido", "república centroafricana", "república checa",
    "república del congo", "república democrática del congo",
    "república dominicana", "ruanda", "rumanía", "rusia", "samoa",
    "san cristóbal y nieves", "san marino", "san vicente y las granadinas",
    "santa lucía", "santo tomé y príncipe", "senegal", "serbia",
    "seychelles", "sierra leona", "singapur", "siria", "somalia",
    "sri lanka", "sudáfrica", "sudán", "sudán del sur", "suecia", "suiza",
    "surinam", "tailandia", "tanzania", "tayikistán", "timor oriental",
    "togo", "tonga", "trinidad y tobago", "túnez", "turkmenistán",
    "turquía", "tuvalu", "ucrania", "uganda", "uruguay", "uzbekistán",
    "vanuatu", "vaticano", "venezuela", "vietnam", "yemen", "yibuti",
    "zambia", "zimbabue",
}

KNOWN_GENRES = {
    "acción", "animación", "aventuras", "bélica", "biográfica",
    "ciencia ficción", "cine negro", "comedia", "comedia dramática",
    "comedia musical", "comedia romántica", "cortometraje", "documental",
    "drama", "erótica", "fantástico", "fantasía", "familiar", "histórica",
    "intriga", "musical", "misterio", "romance", "suspense", "terror",
    "thriller", "western", "policíaca", "deportiva", "religiosa",
}