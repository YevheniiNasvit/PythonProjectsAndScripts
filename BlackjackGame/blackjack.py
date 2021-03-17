import random

#Card attribures
suits = ('Clubs', 'Hearts', 'Spades', 'Diamonds')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#Game variable
full_game = True

class Card:

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.value = values[rank]

	def __str__(self):
		return f'{self.rank} of {self.suit}'

class Deck:

	def __init__(self):
		self.all_cards = []

		for rank in ranks:
			for suit in suits:
				self.all_cards.append(Card(rank, suit))

	def shuffle(self):
		random.shuffle(self.all_cards)

	def deal_one(self):
		return self.all_cards.pop()

class Player:

	def __init__(self, name):
		self.name = name
		self.all_cards = []
		self.bank = 100
		self.total_value = 0

	def show_one_card(self):
		return self.all_cards[0]

	def show_all_cards(self):
		for card in self.all_cards:
			print(card, end = " ")

	def check_for_ace(self):
		return self.all_cards[-1].value == 11

	def value_for_ace(self):
		self.all_cards[-1].value = 1
		self.total_value -= 10

	def hit(self, card):
		self.all_cards.append(card)
		self.total_value += self.all_cards[-1].value

	def show_total_sum(self):
		return self.total_value

	def check_bust(self):
		return self.total_value > 21

	def check_value_in_range_17_21(self):
		return self.total_value in range(17, 21)

	def check_for_21(self):
		return self.total_value == 21

	def take_bet(self):
		while True:
			bet = input('\nPlace your bet on the table\n')
			if bet.isdigit() and (int(bet) % 10 == 0) and int(bet) > 0:
				if (self.bank - int(bet)) < 0:
					print(f'\nNot enough funds! You have {self.bank}. Place another bet!\n')
				else:
					self.bank -= int(bet)
					print(f'\nYou have put {bet}. {self.bank} left.\n')
					break
			else:
				print('\nWrong input! Use numbers that are multiples of 10!\n')
				#bet = input('\nPlace your bet on the table\n')
		return int(bet)

	def check_for_empty_bank(self):
		return self.bank == 0

	def charge_money(self, value):
		self.bank += value

	def set_total_value_to_0(self):
		self.total_value = 0

	def set_empty_all_cards_list(self):
		self.all_cards = []


class Chips:

	def __init__(self):
		self.total = 0

	def add_cash(self, cash):
		self.total += cash 

#-------------------------------------------------------------------------------

def check_dealer_total_value(dealer):
	return dealer >= 17

def check_for_win(total_amount_1, total_amount_2):
	return (total_amount_2 > total_amount_1)

def check_for_draw(total_amount_1, total_amount_2):
	return total_amount_1 == total_amount_2 and total_amount_1 > 0 and total_amount_2 > 0

def take_bank_from_dealer(bank, value):
	bank -= value

def game():

	#While game on
	game_on = True

	while game_on:

		#Create and shuffle new deck
		new_deck = Deck()
		new_deck.shuffle()

		#Create new chips stack
		chips_stack = Chips()

		#Check for empty bank
		if dealer.check_for_empty_bank():
			dealer.charge_money(100)
			print('\nCash was added to dealer!\n')
		if player.check_for_empty_bank():
			print('\nPlayer out of chips!')
			game_on = False
			full_game = False
			break

		#Start a new round---------------------------------------------------------------------------

		#Taking chips from players
		bet = player.take_bet()
		take_bank_from_dealer(dealer.bank, bet)
		chips_stack.add_cash(bet*2) 

		#Deal cards twice to players
		player.hit(new_deck.deal_one())		
		player.hit(new_deck.deal_one())

		dealer.hit(new_deck.deal_one())
		dealer.hit(new_deck.deal_one())

		#Show player's cards at the beginning of the game
		print(f'\nDealer has {dealer.show_one_card()}. Current value is {dealer.all_cards[0].value}\n')
		print('\nPlayer has:')
		player.show_all_cards()
		print(f' Current value is {player.show_total_sum()}\n')
		
		#Variable for player to stay with cards
		stop = False

		#Variable for dealer lost situation
		dealer_lost = False

		#While player is not busted - continue game
		while not player.check_bust() and not dealer_lost:

			#Check blackjack for player and dealer
			if (player.check_for_21() and (dealer.all_cards[0].value == 10 or dealer.all_cards[0].value == 11)):
				print('\nBlack Jack! But dealer can have it too. You can get your bet back, of wait for the game finish.\n')
				answer = input('\nGet bet of wait? Use "get" or "wait"\n')

				while True:
					if answer.lower() == 'get':

						#Get bet and finish game
						print(f'\nDraw! You got {int(chips_stack.total/2)} chips\n')
						dealer.charge_money(int(chips_stack.total/2))
						player.charge_money(int(chips_stack.total/2))
						player.set_total_value_to_0()
						player.set_empty_all_cards_list()
						dealer.set_total_value_to_0()
						dealer.set_empty_all_cards_list()
						game_on = False
						break
					elif answer.lower() == 'wait':

						#Wait for the dealer turn-------------------
						print('\nDealer turn!\n')
						print('\nDealer has:')
						dealer.show_all_cards()
						print(f' Current value is {dealer.show_total_sum()}\n')
						
						#Dealer takes cards until he reaches 17 or more, or bust
						while not check_dealer_total_value(dealer.total_value):
							print('\nDealer takes cards until he will get 17 or higher value!\n')
							dealer.hit(new_deck.deal_one())
							print('\nDealer has:')
							dealer.show_all_cards()
							print(f' Current value is {dealer.show_total_sum()}\n')

							if dealer.check_bust():
								if dealer.check_for_ace():
									dealer.value_for_ace()
									continue
								else:
									print(f'\nDealer busted and lost. You won and got {chips_stack.total} chips\n')
									player.charge_money(chips_stack.total)
									player.set_total_value_to_0()
									player.set_empty_all_cards_list()
									dealer.set_total_value_to_0()
									dealer.set_empty_all_cards_list()
									dealer_lost = True
									game_on = False
									break

						#Final dealer check after he reached 17 and not busted
						
						if dealer.check_for_21():
							print(f'\nDraw, 2 blackjacks! You got {int(chips_stack.total/2)} chips\n')
							dealer.charge_money(int(chips_stack.total/2))
							player.charge_money(int(chips_stack.total/2))
							player.set_total_value_to_0()
							player.set_empty_all_cards_list()
							dealer.set_total_value_to_0()
							dealer.set_empty_all_cards_list()
						elif dealer.check_value_in_range_17_21():
							print(f'\nDealer doesnot have blackjack and lost. You won and got {chips_stack.total} chips\n')
							player.charge_money(chips_stack.total)
							player.set_total_value_to_0()
							player.set_empty_all_cards_list()
							dealer.set_total_value_to_0()
							dealer.set_empty_all_cards_list()
							dealer_lost = True
							game_on = False
							break
							
					elif answer.lower() != 'get' and answer.lower() !='wait':
						print('\nWrong input! Try again!\n')

			#Check blackjack for player
			elif player.check_for_21():
				print(f'\nBlackjack! You win and got {chips_stack.total} chips\n')
				player.charge_money(chips_stack.total)
				player.set_total_value_to_0()
				player.set_empty_all_cards_list()
				dealer.set_total_value_to_0()
				dealer.set_empty_all_cards_list()
				game_on = False
				break

			#Player doesn't have blackjack and can start his hits or stay
			elif (not player.check_for_21() and not player.check_bust() and stop != True):
				player_turn = input('\nTake one more card? Use "y", "yes", "n", or "no" for answer!\n')
				if (player_turn.capitalize() == 'Y') or (player_turn.capitalize() == 'Yes'):
					player.hit(new_deck.deal_one())
					print(f'You got {player.all_cards[-1]}. Current value is {player.show_total_sum()}')
				elif (player_turn.capitalize() == 'N') or (player_turn.capitalize() == 'No'):
					print('\nPlayer has:')
					player.show_all_cards()
					print(f' Current value is {player.show_total_sum()}\n')
					stop = True
				else:
					print('\nWrong input!\n')

			#Player finished his hits and now dealer's turn
			elif stop:
				print('\nDealer turn!\n')
				print('\nDealer has:')
				dealer.show_all_cards()
				print(f' Current value is {dealer.show_total_sum()}\n')
						
				#Dealer takes cards until he reaches 17 or more, or bust
				while not check_dealer_total_value(dealer.total_value):
					print('\nDealer takes cards until he will get 17 or higher value!\n')
					dealer.hit(new_deck.deal_one())
					print('\nDealer has:')
					dealer.show_all_cards()
					print(f' Current value is {dealer.show_total_sum()}\n')

					if dealer.check_bust():
						if dealer.check_for_ace():
							dealer.value_for_ace()
							print('\nDealer has:')
							dealer.show_all_cards()
							print(f' Current value is {dealer.show_total_sum()}\n')
						else:
							print(f'\nDealer busted and lost. You won and got {chips_stack.total} chips\n')
							player.charge_money(chips_stack.total)
							player.set_total_value_to_0()
							player.set_empty_all_cards_list()
							dealer.set_total_value_to_0()
							dealer.set_empty_all_cards_list()
							dealer_lost = True
							game_on = False
							break

				#Final dealer check after he reached 17 and not busted

				# Does dealer has blackjack
				if dealer.check_for_21():
					print('\nBlackjack for dealer! You lost!\n')
					dealer.charge_money(chips_stack.total)
					player.set_total_value_to_0()
					player.set_empty_all_cards_list()
					dealer.set_total_value_to_0()
					dealer.set_empty_all_cards_list()
					game_on = False
					break
				elif not dealer.check_for_21():

					#Compare total sums of player and dealer
					if check_for_win(player.show_total_sum(), dealer.show_total_sum()):
						print('\nYou lost! Dealer has greater value than you!\n')
						dealer.charge_money(chips_stack.total)
						player.set_total_value_to_0()
						player.set_empty_all_cards_list()
						dealer.set_total_value_to_0()
						dealer.set_empty_all_cards_list()
						game_on = False
						break
					elif check_for_win(dealer.show_total_sum(), player.show_total_sum()):
						print(f'\nDealer has lower value and lost. You won and got {chips_stack.total} chips\n')
						player.charge_money(chips_stack.total)
						player.set_total_value_to_0()
						player.set_empty_all_cards_list()
						dealer.set_total_value_to_0()
						dealer.set_empty_all_cards_list()
						dealer_lost = True
						game_on = False
						break
					elif check_for_draw(dealer.show_total_sum(), player.show_total_sum()):
						print(f'\nDraw, same value! You got {int(chips_stack.total/2)} chips\n')
						dealer.charge_money(int(chips_stack.total/2))
						player.charge_money(int(chips_stack.total/2))
						player.set_total_value_to_0()
						player.set_empty_all_cards_list()
						dealer.set_total_value_to_0()
						dealer.set_empty_all_cards_list()
						game_on = False
						break
		if player.check_bust():

			#If ace was the last card in bust situation
			if player.check_for_ace():
				player.value_for_ace()
			else:
				#Player busted
				print('\nYou are busted and lost!\n')
				dealer.charge_money(chips_stack.total)
				player.set_total_value_to_0()
				player.set_empty_all_cards_list()
				dealer.set_total_value_to_0()
				dealer.set_empty_all_cards_list()
				game_on = False
				break


#Start game

#Game setup
dealer = Player('Dealer')
player = Player('Player')

#while full game True
while full_game:

	game_start = input('\nDo you want to start a new game?\n')
	if game_start.capitalize() == 'N' or game_start.capitalize() == 'No':
		full_game = False
		break
	if game_start.capitalize() == 'Y' or game_start.capitalize == 'Yes':
		print('Starting new game!\n')
		game()
	else:
		print('Wrong input! Try again!\n')
		continue