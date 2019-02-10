# Choices

MALE = 'M'
FEMALE = 'F'
UNKNOWN = 'U'
ADMIN = 'A'
DEVELOPER = 'D'
PLAYER = 'P'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (UNKNOWN, 'Unknown'),
)
ROLE_CHOICES = (
    (ADMIN, 'Admin'),
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

sid = 'MusVinAle'
secret_key = '510ed4cc72a95c1972a18cedc5d16318'