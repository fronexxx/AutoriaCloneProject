from better_profanity import profanity
from core.constants.choices import StatusChoices

from .email_service import EmailService

profanity.load_censor_words_from_file('bad_words.txt')


def profanity_validation(listing):
    text = f'{listing.title} {listing.description}'.lower()

    has_bad_words = profanity.contains_profanity(text)

    if has_bad_words:
        listing.is_clean = False
        listing.status = StatusChoices.PENDING
        listing.edit_attempts += 1
        if listing.edit_attempts >= 3:
            listing.status = StatusChoices.INACTIVE
            EmailService.send_profanity_error_emai(listing)
        else:
            listing.status = StatusChoices.PENDING

    else:
        listing.status = StatusChoices.ACTIVE
        listing.is_clean = True

    listing.save()
