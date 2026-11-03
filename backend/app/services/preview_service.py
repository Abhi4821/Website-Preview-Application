import ipaddress
import socket
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


MAX_RESPONSE_BYTES = 2_000_000
TIMEOUT_SECONDS = 12


def _validate_public_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Only valid http:// and https:// URLs are supported.")

    host = parsed.hostname.lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost") or host.endswith(".local"):
        raise ValueError("Local and internal hostnames are not allowed.")

    try:
        addresses = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
    except socket.gaierror:
        raise ValueError("The website hostname could not be resolved.")

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            raise ValueError("Private, local, and reserved IP addresses are not allowed.")


def fetch_preview(url: str) -> dict[str, str | None]:
    current_url = url
    headers = {"User-Agent": "WebsitePreviewAssignment/1.0 (+metadata preview)"}

    # Manually validate each redirect target rather than following unchecked redirects.
    with httpx.Client(timeout=TIMEOUT_SECONDS, follow_redirects=False, headers=headers) as client:
        for _ in range(5):
            _validate_public_http_url(current_url)
            response = client.get(current_url)
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("location")
                if not location:
                    break
                current_url = urljoin(current_url, location)
                continue
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type.lower():
                raise ValueError("The submitted URL does not return an HTML page.")
            if len(response.content) > MAX_RESPONSE_BYTES:
                raise ValueError("The website response is too large to preview.")
            html = response.text
            break
        else:
            raise ValueError("The website redirected too many times.")
    if "html" not in locals():
        raise ValueError("Could not retrieve website preview.")

    soup = BeautifulSoup(html, "html.parser")

    def meta(*keys: str) -> str | None:
        for key in keys:
            tag = soup.find("meta", attrs={"property": key}) or soup.find("meta", attrs={"name": key})
            if tag and tag.get("content"):
                return str(tag["content"]).strip()
        return None

    title = meta("og:title", "twitter:title")
    if not title and soup.title and soup.title.string:
        title = soup.title.string.strip()

    description = meta("og:description", "description", "twitter:description")
    image = meta("og:image", "twitter:image")
    if image:
        image = urljoin(current_url, image)

    site_name = meta("og:site_name")
    parsed = urlparse(current_url)
    favicon_tag = soup.find("link", rel=lambda value: value and "icon" in value)
    favicon = urljoin(current_url, favicon_tag.get("href")) if favicon_tag and favicon_tag.get("href") else f"{parsed.scheme}://{parsed.netloc}/favicon.ico"

    return {
        "url": current_url,
        "title": title or parsed.netloc,
        "description": description or "No description is available for this website.",
        "image_url": image,
        "favicon_url": favicon,
        "site_name": site_name or parsed.netloc,
    }
