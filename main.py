import click
import tweepy
import configparser 
import csv
from datetime import datetime

CONFIG_FILENAME = 'config.ini'

config = configparser.ConfigParser(interpolation=None)
config.read(CONFIG_FILENAME)
bearer_token = config['Twitter']['BEARER_TOKEN']

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

USERNAME = 'rachelnotley'

TODAY = datetime.utcnow()

# Which fields to track for a user
USER_FIELDS = [
            'created_at',
            'description',
            'profile_image_url',
            'public_metrics',
            'verified'
]

@click.command()
@click.argument('handle')
def get_followers(handle):
    """Gets the followers for a given Twitter handle, i.e. jack """

    # Strip "@" off front if used
    if handle[0] == '@':
        handle = handle[1:]

    user = User.fetch_from_username(handle)

    followers = user.fetch_followers()

    with open(f'{TODAY.strftime("%Y-%m-%d_%H%M")}_{handle}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(User.serialized_field_names)

        for follower in followers:
            writer.writerow(follower)

class User:
    """Represents a Twitter User"""

    def __init__(self, response_data):
        self.id = response_data.id
        self.username = response_data.username
        self.description = response_data.description
        self.created_at = response_data.created_at.replace(tzinfo=None)
        self.verified = response_data.verified
        self.profile_image_url = response_data.profile_image_url
        self.followers_count = response_data.public_metrics['followers_count']
        self.following_count = response_data.public_metrics['following_count']
        self.tweet_count = response_data.public_metrics['tweet_count']

    def fetch_followers(self):
        """Returns all the followers for this user"""
        for response in tweepy.Paginator(client.get_users_followers, id=self.id, user_fields = USER_FIELDS, max_results = 1000):
            for follower in response.data:
                yield User(follower)
    
    def account_age_days(self):
        diff = TODAY - self.created_at
        return diff.days

    @property
    def url(self):
        return f'https://www.twitter.com/{self.username}'

    @staticmethod
    def fetch_from_username(username):
        response = client.get_user(username=username, user_fields = USER_FIELDS)
        return User(response.data)

    serialized_field_names = [
            'id',
            'username',
            'url',
            'created_at',
            'verified',
            'description',
            'profile_image_url',
            'followers_count',
            'following_count',
            'tweet_count',
            'account_age_days'
        ]

    def __iter__(self):
        return iter([
            self.id,
            self.username,
            self.url,
            self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            self.verified,
            self.description.replace('\n',''), # Remove any line breaks from the user's description for better CSV formatting
            self.profile_image_url,
            self.followers_count,
            self.following_count,
            self.tweet_count,
            self.account_age_days()
        ])


if __name__ == '__main__': 
    get_followers()


