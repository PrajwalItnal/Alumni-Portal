import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_portal.settings')
django.setup()

from user.models import User, Donation
from decimal import Decimal

def add_donations():
    # Get the alumni user
    try:
        alumni_user = User.objects.get(register_id='ALU001', role='Alumni')
        print(f"Found alumni user: {alumni_user.username}")
    except User.DoesNotExist:
        print("Alumni user not found. Please run setup_test_users.py first.")
        return

    # Create two donations
    donation1 = Donation.objects.create(
        donated_by=alumni_user,
        amount=Decimal('500.00'),
        payment_method='Credit Card',
        description='Donation for student scholarships'
    )
    print(f"Created donation 1: {donation1}")

    donation2 = Donation.objects.create(
        donated_by=alumni_user,
        amount=Decimal('750.00'),
        payment_method='Bank Transfer',
        description='Support for alumni events and networking'
    )
    print(f"Created donation 2: {donation2}")

    print("Donations added successfully!")

if __name__ == "__main__":
    add_donations()