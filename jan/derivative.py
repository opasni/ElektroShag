def deriv3(xl, xr, h=0.02):
    """"
    Sprejme dve tocki oddaljeni za 2h, vrne vrednost na sredini!
    xl    tocka pri x-h
    xr    tocka pri x+h
    """
    return (xr - xl)/2/h