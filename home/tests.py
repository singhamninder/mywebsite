from datetime import date
from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from home.models import Project, Publication, RelatedPublication, Work

OPENALEX_WORKS_PAGE = {
    "results": [
        {
            "id": "https://openalex.org/W111",
            "doi": "https://doi.org/10.1000/example1",
            "title": "Paper One",
            "publication_year": 2023,
            "authorships": [{"author": {"display_name": "Alice Example"}}],
            "primary_location": {
                "landing_page_url": "https://example.com/one",
                "source": {"display_name": "Journal A"},
            },
        },
        {
            "id": "https://openalex.org/W222",
            "doi": "https://doi.org/10.1000/example2",
            "title": "Paper Two",
            "publication_year": 2021,
            "authorships": [{"author": {"display_name": "Bob Example"}}],
            "primary_location": {
                "landing_page_url": "https://example.com/two",
                "source": {"display_name": "Journal B"},
            },
        },
    ],
    "meta": {"next_cursor": None},
}


def mock_openalex_get(url, params=None, timeout=None):
    """Return a fake OpenAlex works response."""
    response = Mock()
    response.raise_for_status = Mock()
    response.json.return_value = OPENALEX_WORKS_PAGE
    return response


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


class ProjectReferencesTests(TestCase):
    """Verify project page renders linked and free-text references."""

    def test_project_page_shows_linked_and_related_publications(self):
        """Both M2M publications and RelatedPublication entries appear under References."""
        project = Project.objects.create(title="Test Project")
        linked = Publication.objects.create(
            title="Linked Paper",
            link="https://example.com/linked",
            year=2024,
        )
        project.publications.add(linked)
        RelatedPublication.objects.create(
            project=project,
            title="Third Party Paper",
            url="https://example.com/third-party",
        )

        response = self.client.get(reverse("project", kwargs={"pk": project.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "References")
        self.assertContains(response, "Linked Paper")
        self.assertContains(response, "Third Party Paper")
        self.assertContains(response, "(2024)")


class SyncPublicationsTests(TestCase):
    """Verify OpenAlex sync command upserts publications idempotently."""

    @patch("home.management.commands.sync_publications.requests.get", side_effect=mock_openalex_get)
    def test_sync_creates_publications_from_openalex(self, _mock_get):
        """Empty database receives two openalex-sourced publications."""
        stdout = StringIO()
        call_command("sync_publications", author_id="A123", stdout=stdout)

        self.assertEqual(Publication.objects.count(), 2)
        paper_one = Publication.objects.get(openalex_id="W111")
        self.assertEqual(paper_one.source, "openalex")
        self.assertEqual(paper_one.year, 2023)
        self.assertEqual(paper_one.doi, "https://doi.org/10.1000/example1")
        self.assertIn("created=2", stdout.getvalue())

    @patch("home.management.commands.sync_publications.requests.get", side_effect=mock_openalex_get)
    def test_sync_is_idempotent(self, _mock_get):
        """Running sync twice does not duplicate publications."""
        call_command("sync_publications", author_id="A123")
        stdout = StringIO()
        call_command("sync_publications", author_id="A123", stdout=stdout)

        self.assertEqual(Publication.objects.count(), 2)
        self.assertIn("created=0", stdout.getvalue())

    @patch("home.management.commands.sync_publications.requests.get", side_effect=mock_openalex_get)
    def test_sync_adopts_manual_publication_with_matching_doi(self, _mock_get):
        """A manual row with the same DOI is updated instead of duplicated."""
        manual_match = Publication.objects.create(
            title="Old Title",
            doi="https://doi.org/10.1000/example1",
            source="manual",
        )
        manual_other = Publication.objects.create(
            title="Unrelated Manual Paper",
            source="manual",
        )

        call_command("sync_publications", author_id="A123")

        self.assertEqual(Publication.objects.count(), 3)
        manual_match.refresh_from_db()
        manual_other.refresh_from_db()
        self.assertEqual(manual_match.openalex_id, "W111")
        self.assertEqual(manual_match.title, "Paper One")
        self.assertEqual(manual_other.openalex_id, None)
        self.assertEqual(manual_other.title, "Unrelated Manual Paper")
        self.assertTrue(Publication.objects.filter(openalex_id="W222").exists())
