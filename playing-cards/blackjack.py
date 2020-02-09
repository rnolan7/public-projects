import random

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


class BlackJack:
    def __init__(self,cash,**kwargs):
        self.cash = cash

        # decide which seat position to take 0-6
        # seat zero is dealt cards first
        # seat six is dealt cards last
        self.seat = kwargs.pop('seat',random.randint(0,6))
        if self.seat < 1 or self.seat > 6:
            self.seat = random.randint(1,6)

        # set number of players
        self.players = kwargs.pop('players',random.randint(1,7))
        if self.players < 1 or self.players > 7:
            self.players = random.randint(1,7)

        # seat players at table
        chairs = [0,1,2,3,4,5,6]
        self.chairs = [0,0,0,0,0,0,0]
        chairs.pop(self.seat)
        self.chairs[self.seat] = 1
        player = 2
        for p in range(self.players - 1):
            pos = chairs.pop(random.randint(0,len(chairs)-1))
            self.chairs[pos] = player
            player += 1


        # get number of decks in shoe
        self.decks = kwargs.pop('decks', 8)

        cut = kwargs.pop('cut', random.randint(1, self.decks*52 - 1))
        self.new_shoe(cut=cut)


    def rulebook(self,hand,dealer_showing):
        recommendation = ''
        hand_val = self.hand_value(hand)
        if len(hand_val) == 1:
            val = hand_val[0]
            if len(hand) == 2 and hand[0][1:] == hand[1][1:]:
                if hand[0][1:] in ('A','8'):
                    recommendation = 'split'
                    return recommendation
                elif hand[0][1:] == '9' and dealer_showing[1:] in ('2','3','4','5','6','8','9'):
                    recommendation = 'split'
                    return recommendation
                elif hand[0][1:] == '7' and dealer_showing[1:] in ('2', '3', '4', '5', '6', '7'):
                    recommendation = 'split'
                    return recommendation
                elif hand[0][1:] == '6' and dealer_showing[1:] in ('2', '3', '4', '5', '6'):
                    recommendation = 'split'
                    return recommendation
                elif hand[0][1:] == '4' and dealer_showing[1:] in ('5', '6'):
                    recommendation = 'split'
                    return recommendation
                elif hand[0][1:] in ('2','3') and dealer_showing[1:] in ('2', '3', '4', '5', '6'):
                    recommendation = 'split'
                    return recommendation
            if val >= 17:
                recommendation = 'stay'
                return recommendation
            elif dealer_showing[1:] in ('2','3','4','5','6') and val >= 13:
                recommendation = 'stay'
                return recommendation
            elif dealer_showing[1:] in ('4','5','6') and val >= 12:
                recommendation = 'stay'
                return recommendation
            elif dealer_showing[1:] in ('2','3') and val == 12:
                recommendation = 'hit'
                return recommendation
            elif dealer_showing[1:] in ('7','8','9','10','J','Q','K','A') and val >= 12:
                recommendation = 'hit'
                return recommendation
            elif val <= 8:
                recommendation = 'hit'
                return recommendation
            elif val == 11:
                if dealer_showing[1:] == 'A':
                    recommendation = 'hit'
                elif len(hand) == 2:
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return recommendation
            elif val == 10:
                if dealer_showing[1:] in ('A', '10'):
                    recommendation = 'hit'
                elif len(hand) == 2:
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return  recommendation
            elif val == 9:
                if dealer_showing[1:] in ('3', '4', '5', '6'):
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return recommendation
            else:
                return recommendation
        elif len(hand_val) > 1:
            soft_val = max(hand_val)
            if len(hand) == 2 and hand[0][1:] == hand[1][1:]:
                if hand[0][1:] in ('A','8'):
                    recommendation = 'split'
                    return recommendation
            if soft_val >= 19:
                recommendation = 'stay'
                return recommendation
            elif soft_val == 18:
                if dealer_showing[1:] in ('2', '7', '8'):
                    recommendation = 'stay'
                elif dealer_showing[1:] in ('3', '4', '5', '6') and len(hand) == 2:
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return recommendation
            elif soft_val == 17:
                if dealer_showing[1:] in ('3', '4', '5', '6') and len(hand) == 2:
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return recommendation
            elif soft_val in (15, 16):
                if dealer_showing[1:] in ('4', '5', '6') and len(hand) == 2:
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return recommendation
            elif soft_val in (13, 14):
                if dealer_showing[1:] in ('5', '6') and len(hand) == 2:
                    recommendation = 'double'
                else:
                    recommendation = 'hit'
                return recommendation
            else:
                return recommendation
        else:
            return recommendation



    def new_shoe(self,**kwargs):
        cards = cards52 * self.decks
        random.shuffle(cards)
        self.deck = cards

        # cut deck (optional)
        cut = kwargs.pop('cut', random.randint(1, len(self.deck) - 1))
        if cut == 0 or cut >= len(self.deck) or cut == False:
            print('skipping cut.')
        else:
            self.deck = self.deck[cut:] + self.deck[:cut]

        # determine when to move to a new shoe
        self.reshuffle = random.randint(10 + len(self.deck) // 2, len(self.deck) - 1)

        self.used_cards = 0
        self.count = 0
        self.hands = []
        self.hand = []
        self.dealers_hand = []
        self.bet = 0


    def update_count(self, card):
        value = card[1:]
        if value in ('10','J','Q','K','A'):
            self.count = self.count - 1
        elif value in ('2','3','4','5','6'):
            self.count = self.count + 1


    def hand_value(self,hand):
        values = [0]
        for card in hand:
            num = card[1:]
            if num in ('10', 'J', 'Q', 'K'):
                for i in range(len(values)):
                    values[i] = values[i] + 10
            elif num == 'A':
                for i in range(len(values)):
                    v = values[i]
                    v1 = v+1
                    values[i] = v+1
                    v2 = v+11
                    if v2 <= 21:
                        values.append(v2)
            else:
                for i in range(len(values)):
                    values[i] = values[i] + int(num)
        if len(values) > 1 and min(values) <= 21 and max(values) > 21:
            for i in range(len(values)-1,-1,-1):
                if values[i] > 21:
                    values.pop(i)
        elif min(values) > 21:
            values = [min(values)]
        values = list(set(values))

        return values


    def deal(self,bet):
        self.bet = bet
        self.cash = self.cash - bet
        self.hands = []
        self.hand = []
        self.dealers_hand = []
        for i in range(len(self.chairs)):
            if self.chairs[i] == 1:
                card = self.deck.pop(0)
                self.used_cards += 1
                self.update_count(card)
                self.hand.append(card)
                # print('dealer deals you a card: {}'.format(card))
            elif self.chairs[i]:
                card = self.deck.pop(0)
                self.used_cards += 1
                self.update_count(card)
                # print('dealer deals {} to player {}'.format(card, self.chairs[i]))

        card = self.deck.pop(0)
        self.used_cards += 1
        self.update_count(card)
        self.dealers_hand.append(card)

        for i in range(len(self.chairs)):
            if self.chairs[i] == 1:
                card = self.deck.pop(0)
                self.used_cards += 1
                self.update_count(card)
                self.hand.append(card)
                # print('dealer deals you a card: {}'.format(card))
            elif self.chairs[i]:
                card = self.deck.pop(0)
                self.used_cards += 1
                self.update_count(card)
                # print('dealer deals {} to player {}'.format(card,self.chairs[i]))
        self.hands.append(self.hand)

        card = self.deck.pop(0)
        self.used_cards += 1
        self.update_count(card)
        self.dealers_hand.append(card)
        self.play_round()


    def play_round(self):
        for i in range(len(self.chairs)):
            if self.chairs[i] == 1:
                for i in range(len(self.hands)):
                    blackjack = False
                    hand = self.hands[i]
                    payout = self.bet * 2
                    value = self.hand_value(hand)
                    if max(value) == 21 and len(hand) == 2:
                        print('blackjack!')
                        blackjack = True
                        payout = self.bet * 2.5

                    dealer_vals = self.hand_value(self.dealers_hand)
                    if max(dealer_vals) == 21 and len(self.dealers_hand) == 2:
                        print('dealer gets blackjack!')
                        if blackjack:
                            payout = self.bet
                        else:
                            payout = 0
                        self.cash = self.cash + payout
                        return

                    if blackjack == False:
                        while True:
                            value = self.hand_value(hand)
                            print('you have {}: {}'.format(value, hand))
                            print('dealer shows a {}'.format(self.dealers_hand[0]))
                            rec = self.rulebook(hand,self.dealers_hand[0])
                            print('the rulebook recommendation is to',rec)

                            if max(value) == 21:
                                break
                            elif min(value) > 21:
                                print('bust!')
                                payout = 0
                                break
                            else:
                                print('value:', max(self.hand_value(hand)))
                                if len(hand) == 2:
                                    prompt = 'hit, stay, double, or split? >> '
                                elif len(hand) > 2:
                                    prompt = 'hit or stay? >> '
                                elif len(hand) == 1:
                                    hand = self.hit(hand)
                                action = input(prompt)
                                action = str(action).lower()
                                if action == 'hit' or (action == '' and rec == 'hit'):
                                    hand = self.hit(hand)
                                elif action == 'stay' or (action == '' and rec == 'stay'):
                                    self.hands[i] = hand
                                    break
                                elif action == 'double' and len(hand) == 2 or (action == '' and rec == 'double'):
                                    self.cash = self.cash - self.bet
                                    self.bet = self.bet * 2
                                    payout = self.bet * 2
                                    hand = self.hit(hand)
                                    value = self.hand_value(hand)
                                    print('doubled down. Now showing {}'.format(max(value)))
                                    break
                                elif action == 'split' and len(hand) == 2:
                                    self.hands.pop(i)
                                    hand1 = [hand[0],]
                                    hand2 = [hand[1],]
                                    hand1 = self.hit(hand1)
                                    hand2 = self.hit(hand2)
                                    self.hands.append(hand1)
                                    self.hands.append(hand2)
                                    # incomplete

                                else:
                                    print('invalid action')
            elif self.chairs[i]:
                pass
        while True:
            dealer_vals = self.hand_value(self.dealers_hand)
            print('dealers hand:',self.dealers_hand)
            print('dealers value:', dealer_vals)

            if len(dealer_vals) > 1 and max(dealer_vals) == 17:
                self.dealers_hand= self.hit(self.dealers_hand)
            elif len(dealer_vals) == 1 and max(dealer_vals) == 17:
                print('dealer stays with {}'.format(max(dealer_vals)))
                break
            elif min(dealer_vals) > 21:
                print('dealer busts!')
                self.cash = self.cash + payout
                return
            elif max(dealer_vals) > 17:
                print('dealer stays with {}'.format(max(dealer_vals)))
                break
            elif min(dealer_vals) < 17:
                self.dealers_hand = self.hit(self.dealers_hand)

        if payout <= 0:
            pass
        elif blackjack:
            print('you win with a blackjack!')
            self.cash = self.cash + payout
        elif max(value) > max(dealer_vals):
            print('your {} beats the dealers {}'.format(max(value),max(dealer_vals)))
            self.cash = self.cash + payout
        elif max(value) == max(dealer_vals):
            self.cash = self.cash + self.bet
            print('push')
        elif max(value) < max(dealer_vals):
            print('your {} loses to the dealers {}'.format(max(value), max(dealer_vals)))

    def hit(self,hand=None):
        card = self.deck.pop(0)
        self.used_cards += 1
        self.update_count(card)
        if hand:
            hand.append(card)
        return hand


def main():
    starting_cash = 1000
    game = BlackJack(starting_cash, players=1)
    while True:
        print()
        print('you have ${} available'.format(game.cash))
        print('count is {}'.format(game.count))
        action = input('bet for new round? ')
        action = str(action).lower()
        if action in ('no','quit','color up','cash out','done','exit'):
            print('you started with ${} and are walking away with ${}'.format(starting_cash,game.cash))
            break
        else:
            try:
                bet = int(action)
            except:
                print('invalid bet')
            else:
                game.deal(bet)




if __name__ == "__main__":
    main()
