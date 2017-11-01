from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# below needed for newer way to reference user model as setting can be changed
from django.contrib.auth import get_user_model

from django.utils import timezone

import uuid

class GameSet(models.Model):
	# name -> name of GameSet
	name = models.CharField(max_length=1000)
	# author -> user that created
	author = models.ForeignKey(get_user_model())
	# created_date -> datetime of when created
	created_date = models.DateTimeField(default=timezone.now)

	# free_space -> Custom free space value
	free_space = models.CharField(max_length=1000, default="Free")

	# allow_free_space -> are we using a free space or not?
	allow_free_space = models.BooleanField(default=True)

	# ordered_columns -> do we want to use ordered columns or allow random order?
	ordered_columns = models.BooleanField(default=True)
	

	# square_count -> int of all that refer to it, necessary?

	# use_count -> count of games 

	"""
		How would I do that? Would I just make it a boolean that sorted all of the 
		squares by when they were created? How would that work for batch imported
		things? What about things where there is a logical order (sequence of numbers)
		but they weren't created in that same temporal order?
	"""

	def __str__(self):
		elipsis = "..." if len(self.name) > 45 else ""
		return "{}{}".format(self.name[:45].rstrip(), elipsis)

class Square(models.Model):
	# set of tuples to be used for choices in self.column
	COLUMN_CHOICES = (
		("B", "B"),
		("I", "I"),
		("N", "N"),
		("G", "G"),
		("O", "O"),
	)

	# value -> what is this square? "Customer spills drink" or "B-10"?
	value = models.CharField(max_length=1000)

	# column -> which column would this square be sorted to when appropriate?
	column = models.CharField(max_length=1, choices=COLUMN_CHOICES, null=True)

	# author -> user that created, must also own GameSet to add
	author = models.ForeignKey(get_user_model())

	# created_date -> datetime of when created
	created_date = models.DateTimeField(default=timezone.now)

	# game_set -> ForeignKey reference to game that contains this
	game_set = models.ForeignKey(GameSet, on_delete=models.CASCADE)

	
	def __str__(self, with_gameset=True):
		col_format = "{} - ".format(self.column) if self.game_set.ordered_columns else ""
		game_set_format = " in '{}'".format(self.game_set.__str__()) if with_gameset else ""
		return "{}'{}'{}".format(col_format, self.value, game_set_format)

class GameInstance(models.Model):
	# game_set -> foreign key to refer to GameSet in use
	game_set = models.ForeignKey(GameSet, on_delete=models.CASCADE)

	# admin -> reference to user who created this
	admin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	# player_count -> how many players are in the game?
	player_count = models.IntegerField(default=1)

	# users -> OneToMany reference of users participating (upper limit maybe?)

	# game_uuid -> uuid to create link to this game
	game_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	
	# game_created -> datetime of when game was created
	game_created = models.DateTimeField(default=timezone.now)
	
	# game_completed -> datetime of when game was completed
	# I can't remember if this is the proper way to do this.
	# game_completed = model.DateTimeField(null=True)

	def __str__(self):
		return "Game using '{}', created on {} by {}.".format(
																self.game_set.__str__(),
																self.game_created,
																self.admin.__str__(),
															)


class GameCard(models.Model):
	# game_instance -> foreign key for game that this card is part of
	game_instance = models.ForeignKey(GameInstance, on_delete=models.CASCADE)
	# owner -> foreign key for user that owns this, can be null if playing without registered users
	owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
	# player_name -> player name for this card. defaults to "Player".
		# this should actually grab the name from the owner if they are registered, but
		# I'm going to default them all to Player for now. the idea would be that non-registered users
		# could have a custom name in the game.
	player_name = models.CharField(max_length=64, default="Player")
	# used to link to this game.
	game_card_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	def __str__(self):
		return "Bingo Card - {}".format(self.game_card_uuid)


class GameEvent(models.Model):
	# game_instance -> foreign key to refer to GameInstance it was called in
	game_instance = models.ForeignKey(GameInstance, on_delete=models.CASCADE)
	# square_marked -> reference to Square that was marked
	square_marked = models.ForeignKey(Square, on_delete=models.CASCADE)
	# time_marked -> datetime for when Square was marked
	time_marked = models.DateTimeField(default=timezone.now)

	"""
		Here's a potential gotcha we've got going on - a game instance can mark a 
		square that's not contained in the game_set used by the game_instance that 
		it's a part of. 

		How do I enforce this? Is there some sort of 
	"""

	def __str__(self):
		return "Event in Game {} - Square '{}' marked.".format(
											self.game_instance.game_uuid,
											self.square_marked.__str__(with_gameset=False))