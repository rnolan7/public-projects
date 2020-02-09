class Card:
    def __init__(self, id, **kwargs):
        _suits = {
            'H': 'Hearts',
            'D': 'Diamonds',
            'C': 'Clubs',
            'S': 'Spades',
        }
        _vals = {
            '2': ((2,), 'Two'),
            '3': ((3,), 'Three'),
            '4': ((4,), 'Four'),
            '5': ((5,), 'Five'),
            '6': ((6,), 'Six'),
            '7': ((7,), 'Seven'),
            '8': ((8,), 'Eight'),
            '9': ((9,), 'Nine'),
            '10': ((10,), 'Ten'),
            'J': ((10,), 'Jack'),
            'Q': ((10,), 'Queen'),
            'K': ((10,), 'King'),
            'A': ((11, 1), 'Ace'),
        }
        self.id = id
        self.suit = ''
        self.verbose_value = ''
        self.value = 0
        self.description = ''
        if type(id) != str:
            raise ValueError(self.id, 'is an invalid id for card class')
        elif len(id) != 2 and len(id) != 3:
            raise ValueError(self.id, 'is an invalid id for card class')
        try:
            self.suit = _suits[id[0]]
        except:
            raise ValueError(self.id, 'is an invalid id for card class')
        try:
            self.value = _vals[id[1:]][0]
            self.verbose_value = _vals[id[1:]][1]
        except:
            raise ValueError(self.id, 'is an invalid id for card class')
        self.description = '{} of {}'.format(self.verbose_value,self.suit)


if __name__ == "__main__":
    cards52 = [
        'HA', 'DA', 'CA', 'SA',
        'H2', 'D2', 'C2', 'S2',
        'H3', 'D3', 'C3', 'S3',
        'H4', 'D4', 'C4', 'S4',
        'H5', 'D5', 'C5', 'S5',
        'H6', 'D6', 'C6', 'S6',
        'H7', 'D7', 'C7', 'S7',
        'H8', 'D8', 'C8', 'S8',
        'H9', 'D9', 'C9', 'S9',
        'H10', 'D10', 'C10', 'S10',
        'HJ', 'DJ', 'CJ', 'SJ',
        'HQ', 'DQ', 'CQ', 'SQ',
        'HK', 'DK', 'CK', 'SK',
    ]
    newList = []
    for c in cards52:
        newList.append(Card(c))
    print(newList)
    print(newList[5].id)
    print(newList[5].description)
    print(newList[5].suit)
    print(newList[5].verbose_value)
    print(newList[5].value)

