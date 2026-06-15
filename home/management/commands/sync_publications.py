from typing import Any

import requests
from django.core.management.base import BaseCommand, CommandError

from home.models import Info, Publication

OPENALEX_BASE = "https://api.openalex.org"
REQUEST_TIMEOUT = 30


def strip_openalex_id(openalex_url: str | None) -> str | None:
    """Return the short OpenAlex id (e.g. W123) from a full URL."""
    if not openalex_url:
        return None
    return openalex_url.rstrip("/").rsplit("/", 1)[-1]


def normalize_doi(doi: str | None) -> str | None:
    """Keep a full https://doi.org/... URL, or None."""
    if not doi:
        return None
    if doi.startswith("http"):
        return doi
    return f"https://doi.org/{doi.removeprefix('doi:').lstrip('/')}"


def work_to_publication_fields(work: dict[str, Any]) -> dict[str, Any] | None:
    """Map an OpenAlex work JSON object to Publication field values."""
    title = work.get("title") or work.get("display_name")
    if not title:
        return None

    openalex_id = strip_openalex_id(work.get("id"))
    doi = normalize_doi(work.get("doi"))

    authors = ", ".join(
        authorship["author"]["display_name"]
        for authorship in work.get("authorships", [])
        if authorship.get("author", {}).get("display_name")
    )

    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    venue = source.get("display_name") or ""

    link = primary_location.get("landing_page_url") or doi or work.get("id")

    return {
        "openalex_id": openalex_id,
        "doi": doi,
        "title": title,
        "year": work.get("publication_year"),
        "authors": authors,
        "venue": venue,
        "link": link,
    }


class Command(BaseCommand):
    """Upsert publications from OpenAlex for the site owner's author profile."""

    help = "Sync publications from OpenAlex into the Publication table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--author-id",
            dest="author_id",
            help="OpenAlex author id (e.g. A5023888391). Overrides Info.openalex_author_id.",
        )

    def handle(self, *args, **options):
        info = Info.objects.first()
        author_id = self._resolve_author_id(options.get("author_id"), info)
        mailto = str(info.email) if info and info.email else ""

        created = 0
        updated = 0
        skipped = 0

        for work in self._fetch_works(author_id, mailto):
            fields = work_to_publication_fields(work)
            if fields is None:
                skipped += 1
                continue

            publication, was_created = self._upsert_publication(fields)
            if was_created:
                created += 1
            else:
                updated += 1

        summary = f"created={created} updated={updated} skipped={skipped}"
        self.stdout.write(summary)

    def _resolve_author_id(self, cli_author_id: str | None, info: Info | None) -> str:
        """Resolve OpenAlex author id from CLI, Info, or ORCID lookup."""
        if cli_author_id:
            return strip_openalex_id(cli_author_id) or cli_author_id

        if info and info.openalex_author_id:
            return info.openalex_author_id.strip()

        if info and info.orcid:
            return self._author_id_from_orcid(info.orcid.strip(), str(info.email or ""))

        raise CommandError(
            "No OpenAlex author id available. Set Info.openalex_author_id or Info.orcid "
            "in the admin, or pass --author-id."
        )

    def _author_id_from_orcid(self, orcid: str, mailto: str) -> str:
        """Look up an OpenAlex author id from an ORCID."""
        params: dict[str, str] = {}
        if mailto:
            params["mailto"] = mailto

        response = requests.get(
            f"{OPENALEX_BASE}/authors/orcid:{orcid}",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        author_id = strip_openalex_id(response.json().get("id"))
        if not author_id:
            raise CommandError(f"Could not resolve OpenAlex author id from ORCID {orcid!r}.")
        return author_id

    def _fetch_works(self, author_id: str, mailto: str):
        """Yield all works for an author, following cursor pagination."""
        cursor = "*"
        while cursor:
            params: dict[str, str] = {
                "filter": f"author.id:{author_id}",
                "per-page": "200",
                "cursor": cursor,
            }
            if mailto:
                params["mailto"] = mailto

            response = requests.get(
                f"{OPENALEX_BASE}/works",
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()

            yield from payload.get("results", [])
            cursor = payload.get("meta", {}).get("next_cursor")

    def _upsert_publication(self, fields: dict[str, Any]) -> tuple[Publication, bool]:
        """Create or update a publication matched by openalex_id then doi."""
        openalex_id = fields["openalex_id"]
        doi = fields["doi"]

        publication = None
        if openalex_id:
            publication = Publication.objects.filter(openalex_id=openalex_id).first()
        if publication is None and doi:
            publication = Publication.objects.filter(doi=doi).first()

        update_fields = {
            "title": fields["title"],
            "year": fields["year"],
            "authors": fields["authors"],
            "venue": fields["venue"],
            "link": fields["link"],
            "openalex_id": openalex_id,
        }

        if publication is None:
            publication = Publication.objects.create(
                **update_fields,
                doi=doi,
                source="openalex",
            )
            return publication, True

        for attr, value in update_fields.items():
            setattr(publication, attr, value)
        if doi and publication.doi != doi:
            publication.doi = doi
        publication.save()
        return publication, False
