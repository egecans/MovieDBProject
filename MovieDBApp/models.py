from django.db import models

class DatabaseManager(models.Model):
    password = models.CharField(max_length=20)
    manager_username = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'database_manager'

class Audience(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'audience'

class Director(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)
    nation = models.CharField(max_length=20)
    platform = models.ForeignKey('Platform', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'director'


class Platform(models.Model):
    platform_name = models.CharField(unique=True, max_length=20)
    platform_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'platform'

    def __str__(self):     #add this to view the platforms with their name instead of object id
        return self.platform_name

class Agreement(models.Model): #relationship between director and platform
    username = models.OneToOneField('Director', models.DO_NOTHING, db_column='username', primary_key=True)  # The composite primary key (username, platform_id) found, that is not supported. The first column is selected.
    platform = models.ForeignKey('Platform', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'agreement'
        unique_together = (('username', 'platform'),)

class Subscribe(models.Model): #relationship between user and platform
    username = models.OneToOneField(Audience, models.DO_NOTHING, db_column='username', primary_key=True)  # The composite primary key (username, platform_id) found, that is not supported. The first column is selected.
    platform = models.ForeignKey(Platform, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subscribe'
        unique_together = (('username', 'platform'),)

class DirectedMovie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    movie_name = models.CharField(max_length=20)
    duration = models.IntegerField(blank=True, null=True)
    username = models.ForeignKey('Director', models.DO_NOTHING, db_column='username')
    avg_rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'directed_movie'


class Rate(models.Model): #relationship between audience and movie
    username = models.OneToOneField(Audience, models.DO_NOTHING, db_column='username', primary_key=True)  # The composite primary key (username, movie_id) found, that is not supported. The first column is selected.
    movie = models.ForeignKey(DirectedMovie, models.DO_NOTHING)
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'rate'
        unique_together = (('username', 'movie'),)


class NextTo(models.Model): #movie and movie relationship
    pre = models.OneToOneField(DirectedMovie, models.DO_NOTHING, primary_key=True)  # The composite primary key (pre_id, suc_id) found, that is not supported. The first column is selected.
    suc = models.ForeignKey(DirectedMovie, models.DO_NOTHING, related_name='nextto_suc_set')

    class Meta:
        managed = False
        db_table = 'next_to'
        unique_together = (('pre', 'suc'),)


class Genre(models.Model):
    genre_name = models.CharField(unique=True, max_length=20)
    genre_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'genre'


class Classify(models.Model): #relationship betweeen movie and genre
    movie = models.OneToOneField('DirectedMovie', models.DO_NOTHING, primary_key=True)  # The composite primary key (movie_id, genre_id) found, that is not supported. The first column is selected.
    genre = models.ForeignKey('Genre', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classify'
        unique_together = (('movie', 'genre'),)


class MovieSession(models.Model):
    date = models.DateField()
    time_slot = models.IntegerField()
    session_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'movie_session'


class Buy(models.Model): #relationship between session and user
    username = models.OneToOneField(Audience, models.DO_NOTHING, db_column='username', primary_key=True)  # The composite primary key (username, session_id) found, that is not supported. The first column is selected.
    session = models.ForeignKey('MovieSession', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'buy'
        unique_together = (('username', 'session'),)


class Play(models.Model): #relationship between movie and session
    session = models.OneToOneField(MovieSession, models.DO_NOTHING, primary_key=True)  # The composite primary key (session_id, movie_id) found, that is not supported. The first column is selected.
    movie = models.ForeignKey(DirectedMovie, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'play'
        unique_together = (('session', 'movie'),)

class Theatre(models.Model):
    district = models.CharField(max_length=25, blank=True, null=True)
    theatre_name = models.CharField(max_length=25)
    capacity = models.IntegerField(blank=True, null=True)
    theatre_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'theatre'


class Located(models.Model): #relationship between session and theatre
    session = models.OneToOneField('MovieSession', models.DO_NOTHING, primary_key=True)  # The composite primary key (session_id, theatre_id) found, that is not supported. The first column is selected.
    theatre = models.ForeignKey('Theatre', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'located'
        unique_together = (('session', 'theatre'),)
