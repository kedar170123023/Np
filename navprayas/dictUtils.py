""" Allowed Description Fee Payment """

ADFP = {
    "MTSE": {#1
        "allowed"           : True,
        "description"       : "MANPUR TALENT SEARCH EXAM (MTSE)",
        "fee"               : 25,
        "payment_required"  : True,
    },           
    "PR":   {#2
        "allowed"           : True,
        "description"       : "PUZZLE RACE",
        "fee"               : 40,
        "payment_required"  : True,
    },               
    "CC":   {#3
        "allowed"           : True,
        "description"       : "CAREER COUNSELLING",
        "fee"               : 0,
        "payment_required"  : False,
    },           
    "RANGOTSAV":  {#4
        "allowed"           : True,
        "description"       : "RANGOTSAV",
        "fee"               : 0,
        "payment_required"  : False,
    },  
    "FHS":  {#5
        "allowed"           : True,
        "description"       : "FREE HAND SKETCHING",
        "fee"               : 10,
        "payment_required"  : True,
    },       
    "CHESS": {#6
        "allowed"           : True,
        "description"       : "CHESS COMPETITION",
        "fee"               : 10,
        "payment_required"  : True,
    }       
}
""" In choices  """
""" If you don't want to get ----- in values then set a default value to avoid this """

CHOICES = {
    # Gender
    "GENDER"  : (
        ('Female','Female'),
        ('Male','Male'),
    ),
    # Question Paper Language
    "QPL"     : (
        ('English','English'),
        ('Hindi','Hindi'),
    ),
    # Class
    'CLASS'     : (
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ),
    # Board
    "BOARD" : (
        ('BSEB','BSEB'),
        ('CBSE','CBSE'),
    ),
    # chess category
    "C_CATEGORY" : (
        ('G1','Upto 13 yrs'),
        ('G2','From 14 to 17 yrs'),
        ('G3','Above 17 yrs'),
    ),
    "CC_CATEGORY" : (
        ('G1','Upto 10'),
        ('G2','Above 10'),
    ),
    # FHS catergory
    "F_CATEGORY" : (
        ('Junior','V/VI/VII'),
        ('Senior','VIII/IX/X'),
    ),
    # rangostsav category
    "R_CATEGORY" : (
        ('Junior','Below 13 years'),
        ('Senior','Above or equal to 13 yrs'),
    ),
    # 
    # PR category
    "P_CATEGORY" : (
        ('Junior','VII/VIII'),
        ('Senior','IX/X'),
    ),


}