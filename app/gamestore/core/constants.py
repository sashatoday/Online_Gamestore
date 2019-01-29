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
        ('ADVENTURE', 'Adventure'),
        ('ARCADE', 'Arcade'),
        ('FANTASY', 'Fantasy'),
        ('FIGHTING', 'Fighting'),
        ('PUZZLE', 'Puzzle'),
        ('SIMULATION', 'Simulation'),
        ('SPORTS', 'Sports'),
        ('STRATEGY', 'Strategy'),
        ('OTHER', 'Other'),
    )