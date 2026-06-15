from datetime import date

from django.test import TestCase

from home.models import Work


class WorkOrderingTests(TestCase):
    """Verify Work entries sort current roles first, then by date."""

    def test_ongoing_role_sorts_first_then_descending_end_date(self):
        """Ongoing roles precede ended roles; ended roles sort by newest end date."""
        Work.objects.create(
            title="Past Role A",
            place="Org A",
            start_date=date(2018, 1, 1),
            end_date=date(2020, 6, 1),
        )
        Work.objects.create(
            title="Current Role",
            place="Org B",
            start_date=date(2023, 1, 1),
            end_date=None,
        )
        Work.objects.create(
            title="Past Role B",
            place="Org C",
            start_date=date(2020, 7, 1),
            end_date=date(2022, 12, 1),
        )

        titles = list(Work.objects.values_list("title", flat=True))

        self.assertEqual(
            titles,
            ["Current Role", "Past Role B", "Past Role A"],
        )
