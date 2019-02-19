#####################################
### This file contains constants: ###
###      * choices                ###
###      * payment constants      ###
###      * file names             ###
#####################################


#### Choices

MALE = 'M'
FEMALE = 'F'
UNKNOWN = 'U'
DEVELOPER = 'D'
PLAYER = 'P'

GENDER_CHOICES = (
    (UNKNOWN, 'Unknown'),
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)
ROLE_CHOICES = (
    (DEVELOPER, 'Developer'),
    (PLAYER, 'Player'),
)

CATEGORY_CHOICES = (
        ('ACTION', 'Action'),
        ('ACTION-ADVENTURE', 'Action-adventure'),
        ('ADVENTURE', 'Adventure'),
        ('ARCADE', 'Arcade'),
        ('FANTASY', 'Fantasy'),
        ('FIGHTING', 'Fighting'),
        ('PUZZLE', 'Puzzle'),
        ('ROLE-PLAYING', 'Role-playing'),
        ('SIMULATION', 'Simulation'),
        ('SPORTS', 'Sports'),
        ('STRATEGY', 'Strategy'),
        ('OTHER', 'Other'),
    )

SORT_CHOICES = (
        ('name', 'Title abc'),
        ('-name', 'Title cba'),
        ('-date', 'Fresh first'),
        ('date', 'Old first'),
        ('price', 'Low price first'),
        ('-price', 'High price first'),
        ('age_limit', 'Low age limit'),
        ('-age_limit', 'High age limit'),
    )

### Payment constants 
sid = 'MusVinAle'
secret_key = '510ed4cc72a95c1972a18cedc5d16318'

### File names

BASE_HTML = 'base.html'
THANKS_HTML = 'extra/thanks.html'
ERROR_HTML = 'extra/error.html'

ACTIVATE_ACCOUNT_HTML = 'account/restore_account.html'
LOGIN_HTML = 'account/login.html'
SIGNUP_HTML = 'account/signup.html'
PROFILE_HTML = 'account/profile.html'
PROFILE_PREVIEW_HTML = 'account/profile_preview.html'
RESET_PASS_HTML = 'account/reset_password.html'
SET_NEW_PASS_HTML = 'account/set_new_password.html'
USER_AGREEMENT_HTML = 'account/user_agreement.html'

EMAIL_RESET_PASS_HTML = 'email/acc_reset_pass.html'
ACTIVATE_EMAIL_HTML = 'email/acc_active_email.html'
EMAIL_RESTORE_ACCOUNT_HTML = 'email/acc_active_account.html'

SEARCH_GAME_HTML = 'games/search_game.html'
MY_GAMES_HTML = 'games/my_games.html'
WISHLIST_HTML = 'games/wishlist.html'
GAME_DESCRIPTION_HTML = 'games/game_description.html'
BUY_GAME_HTML = 'games/buy_game.html'
PLAY_GAME_HTML = 'games/play_game.html'

UPLOADED_GAMES_HTML = 'developer/uploaded_games.html'
ADD_GAME_HTML = 'developer/add_game.html'
EDIT_GAME_HTML = 'developer/edit_game.html'
GAMES_STATISTICS_HTML = 'developer/games_statistics.html'
DEVELOPER_AGREEMENT_HTML = 'developer/developer_agreement.html'

PAYMENT_SUCCESS_HTML = 'payment/success.html'
PAYMENT_ERROR_HTML = 'payment/error.html'
