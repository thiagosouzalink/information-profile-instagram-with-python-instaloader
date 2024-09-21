from instaloader.structures import Profile

from profile_information import process_information
from get_session_user import instagram


# Username 
# USER = "username"
USER = instagram.context.username

print("Getting profile...")
profile = Profile.from_username(instagram.context, USER)
print("Getting profile information...")
process_information(profile=profile, get_not_followers_back=True)