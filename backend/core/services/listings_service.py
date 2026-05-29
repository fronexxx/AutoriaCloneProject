from datetime import timedelta

from django.utils import timezone

from better_profanity import profanity
from core.constants.choices import StatusChoices

from .email_service import EmailService

profanity.load_censor_words_from_file('bad_words.txt')


class ListingsService:
    @staticmethod
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

    @staticmethod
    def stats_handler(listing, user):
        stats = listing.stats

        now = timezone.now()

        if not stats.last_view_at or stats.last_view_at.date() != now.date():
            stats.views_daily = 0

        if not stats.last_view_at or now - stats.last_view_at > timedelta(days=7):
            stats.views_weekly = 0

        if not stats.last_view_at or now.month != stats.last_view_at.month:
            stats.views_monthly = 0

        if not user.is_authenticated or listing.owner != user:
            stats.views_total += 1
            stats.views_daily += 1
            stats.views_weekly += 1
            stats.views_monthly += 1
            stats.last_view_at = now
            stats.save()
