import ipaddress
import logging
import socket

from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

MAX_RESPONSE_BYTES = 2_000_000
TIMEOUT_SECONDS = 15
MAX_REDIRECTS = 5
MAX_URL_LENGTH = 2048
CHUNK_SIZE = 16_384


def _validate_public_http_url(url: str) -> None:
    if len(url) > MAX_URL_LENGTH:
        raise ValueError("Website URL is too long.")

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Only valid http:// and https:// URLs are supported.")

    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs containing username or password are not allowed.")

    host = parsed.hostname.lower().rstrip(".")

    if (
        host in {"localhost", "localhost.localdomain"}
        or host.endswith(".localhost")
        or host.endswith(".local")
    ):
        raise ValueError("Local and internal hostnames are not allowed.")

    try:
        # Literal IP address or DNS resolution.
        try:
            addresses = [ipaddress.ip_address(host)]
        except ValueError:
            resolved = socket.getaddrinfo(
                host,
                parsed.port or (443 if parsed.scheme == "https" else 80),
                type=socket.SOCK_STREAM,
            )
            addresses = [
                ipaddress.ip_address(item[4][0].split("%")[0])
                for item in resolved
            ]

    except (socket.gaierror, ValueError):
        raise ValueError("The website hostname could not be resolved.")

    if not addresses:
        raise ValueError("The website hostname could not be resolved.")

    for ip in addresses:
        if not ip.is_global:
            raise ValueError(
                "Private, local, and reserved IP addresses are not allowed."
            )


def _fallback_preview(url: str) -> dict[str, str | None]:
    parsed = urlparse(url)

    domain = parsed.hostname or "Unknown Website"
    site_name = domain.removeprefix("www.")

    return {
        "url": url,
        "title": site_name,
        "description": (
            "A preview could not be retrieved automatically. "
            "Visit the website using the original URL."
        ),
        "image_url": None,
        "favicon_url": f"{parsed.scheme}://{parsed.netloc}/favicon.ico",
        "site_name": site_name,
    }


def _read_limited_response(response: httpx.Response) -> bytes | None:
    content_length = response.headers.get("content-length")

    if content_length:
        try:
            if int(content_length) > MAX_RESPONSE_BYTES:
                return None
        except ValueError:
            pass

    content = bytearray()

    for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
        content.extend(chunk)

        if len(content) > MAX_RESPONSE_BYTES:
            return None

    return bytes(content)


def fetch_preview(url: str) -> dict[str, str | None]:
    current_url = url

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    _validate_public_http_url(current_url)

    html = ""

    try:
        with httpx.Client(
            timeout=httpx.Timeout(TIMEOUT_SECONDS),
            follow_redirects=False,
            headers=headers,
            trust_env=False,
        ) as client:

            for redirect_count in range(MAX_REDIRECTS + 1):

                _validate_public_http_url(current_url)

                with client.stream("GET", current_url) as response:

                    if response.status_code in (301, 302, 303, 307, 308):
                        location = response.headers.get("location")

                        if not location:
                            logger.warning(
                                "Redirect without location: %s",
                                current_url,
                            )
                            return _fallback_preview(url)

                        if redirect_count == MAX_REDIRECTS:
                            logger.warning("Too many redirects: %s", url)
                            return _fallback_preview(url)

                        next_url = urljoin(current_url, location)
                        _validate_public_http_url(next_url)
                        current_url = next_url
                        continue

                    if response.status_code >= 400:
                        logger.warning(
                            "Website returned HTTP %s: %s",
                            response.status_code,
                            current_url,
                        )
                        return _fallback_preview(url)

                    content_type = response.headers.get("content-type", "")

                    if "text/html" not in content_type.lower():
                        logger.warning(
                            "Website did not return HTML: %s",
                            current_url,
                        )
                        return _fallback_preview(url)

                    body = _read_limited_response(response)

                    if body is None:
                        logger.warning(
                            "Website response too large: %s",
                            current_url,
                        )
                        return _fallback_preview(url)

                    encoding = response.encoding or "utf-8"

                    try:
                        html = body.decode(encoding, errors="replace")
                    except LookupError:
                        html = body.decode("utf-8", errors="replace")

                    if not html.strip():
                        logger.warning("Empty HTML received: %s", current_url)
                        return _fallback_preview(url)

                    soup_check = BeautifulSoup(html, "html.parser")

                    if (
                        not soup_check.get_text(strip=True)
                        and not soup_check.find("meta")
                    ):
                        logger.warning(
                            "HTML contains no useful content: %s",
                            current_url,
                        )
                        return _fallback_preview(url)

                    break

            else:
                return _fallback_preview(url)

    except ValueError:
        raise

    except httpx.HTTPError as exc:
        logger.warning(
            "Could not fetch website %s: %s",
            current_url,
            exc,
        )
        return _fallback_preview(url)

    except Exception:
        logger.exception(
            "Unexpected preview error for %s",
            current_url,
        )
        return _fallback_preview(url)

    soup = BeautifulSoup(html, "html.parser")

    def meta(*keys: str) -> str | None:
        for key in keys:
            tag = (
                soup.find("meta", attrs={"property": key})
                or soup.find("meta", attrs={"name": key})
            )

            if tag and tag.get("content"):
                value = str(tag["content"]).strip()

                if value:
                    return value

        return None

    title = meta("og:title", "twitter:title")

    if not title and soup.title:
        title = soup.title.get_text(strip=True) or None

    description = meta(
        "og:description",
        "description",
        "twitter:description",
    )

    image = meta("og:image", "twitter:image")

    if image:
        image = urljoin(current_url, image)

    site_name = meta("og:site_name")

    parsed = urlparse(current_url)

    favicon_tag = soup.find(
        "link",
        rel=lambda value: value and "icon" in str(value).lower(),
    )

    favicon = (
        urljoin(current_url, favicon_tag.get("href"))
        if favicon_tag and favicon_tag.get("href")
        else f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
    )

    if not title and not description and not image and not site_name:
        logger.warning("No useful metadata found: %s", current_url)
        return _fallback_preview(url)

    return {
        "url": current_url,
        "title": title or parsed.netloc,
        "description": description or "No description is available for this website.",
        "image_url": image,
        "favicon_url": favicon,
        "site_name": site_name or parsed.netloc,
    }


# import ipaddress
# import socket
# import logging

# from urllib.parse import urljoin, urlparse

# import httpx
# from bs4 import BeautifulSoup


# logger = logging.getLogger(__name__)

# MAX_RESPONSE_BYTES = 2_000_000
# TIMEOUT_SECONDS = 15
# MAX_REDIRECTS = 5


# def _validate_public_http_url(url: str) -> None:
#     parsed = urlparse(url)

#     if parsed.scheme not in ("http", "https") or not parsed.hostname:
#         raise ValueError("Only valid http:// and https:// URLs are supported.")

#     host = parsed.hostname.lower()

#     if (
#         host in {"localhost", "localhost.localdomain"}
#         or host.endswith(".localhost")
#         or host.endswith(".local")
#     ):
#         raise ValueError("Local and internal hostnames are not allowed.")

#     try:
#         addresses = socket.getaddrinfo(
#             host,
#             parsed.port or (443 if parsed.scheme == "https" else 80)
#         )
#     except socket.gaierror:
#         raise ValueError("The website hostname could not be resolved.")

#     for address in addresses:
#         ip = ipaddress.ip_address(address[4][0])

#         if not ip.is_global:
#             raise ValueError("Private, local, and reserved IP addresses are not allowed.")


# def _fallback_preview(url: str) -> dict[str, str | None]:
#     """
#     Generate a fallback preview when a website blocks
#     automated requests or returns empty HTML.
#     """

#     parsed = urlparse(url)

#     domain = parsed.hostname or "Unknown Website"

#     site_name = domain.removeprefix("www.")

#     return {
#         "url": url,
#         "title": site_name,
#         "description": (
#             "A preview could not be retrieved automatically. "
#             "Visit the website using the original URL."
#         ),
#         "image_url": None,
#         "favicon_url": f"{parsed.scheme}://{parsed.netloc}/favicon.ico",
#         "site_name": site_name,
#     }


# def fetch_preview(url: str) -> dict[str, str | None]:

#     current_url = url

#     headers = {
#         "User-Agent": (
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             "AppleWebKit/537.36 (KHTML, like Gecko) "
#             "Chrome/120.0.0.0 Safari/537.36"
#         ),
#         "Accept": (
#             "text/html,application/xhtml+xml,"
#             "application/xml;q=0.9,*/*;q=0.8"
#         ),
#         "Accept-Language": "en-US,en;q=0.9",
#     }

#     # Validate the original URL.
#     _validate_public_http_url(current_url)

#     try:
#         with httpx.Client(
#             timeout=TIMEOUT_SECONDS,
#             follow_redirects=False,
#             headers=headers,
#         ) as client:

#             for redirect_count in range(MAX_REDIRECTS + 1):

#                 response = client.get(current_url)

#                 # Handle redirects manually.
#                 if response.status_code in (301, 302, 303, 307, 308):

#                     location = response.headers.get("location")

#                     if not location:
#                         logger.warning("Redirect without location: %s", current_url)
#                         return _fallback_preview(current_url)

#                     if redirect_count == MAX_REDIRECTS:
#                         logger.warning("Too many redirects: %s", url)
#                         return _fallback_preview(current_url)

#                     current_url = urljoin(current_url, location)

#                     # Validate every redirect destination.
#                     _validate_public_http_url(current_url)

#                     continue

#                 # Handle HTTP errors.
#                 if response.status_code >= 400:
#                     logger.warning(
#                         "Website returned HTTP %s: %s",
#                         response.status_code,
#                         current_url,
#                     )
#                     return _fallback_preview(current_url)

#                 content_type = response.headers.get("content-type", "")

#                 if "text/html" not in content_type.lower():
#                     logger.warning(
#                         "Website did not return HTML: %s",
#                         current_url,
#                     )
#                     return _fallback_preview(current_url)

#                 if len(response.content) > MAX_RESPONSE_BYTES:
#                     logger.warning("Website response too large: %s", current_url)
#                     return _fallback_preview(current_url)

#                 html = response.text

#                 # Handle empty HTML responses.
#                 if not html or not html.strip():
#                     logger.warning("Empty HTML received: %s", current_url)
#                     return _fallback_preview(current_url)

#                 # Handle empty HTML document such as <HTML></HTML>.
#                 soup_check = BeautifulSoup(html, "html.parser")

#                 if not soup_check.get_text(strip=True) and not soup_check.find("meta"):
#                     logger.warning("HTML contains no useful content: %s", current_url)
#                     return _fallback_preview(current_url)

#                 break

#             else:
#                 return _fallback_preview(current_url)

#     except ValueError:
#         # Do not bypass URL validation.
#         raise

#     except httpx.HTTPError as exc:
#         logger.warning(
#             "Could not fetch website %s: %s",
#             current_url,
#             exc,
#         )
#         return _fallback_preview(current_url)

#     except Exception:
#         logger.exception("Unexpected preview error for %s", current_url)
#         return _fallback_preview(current_url)

#     # Extract website metadata.
#     soup = BeautifulSoup(html, "html.parser")

#     def meta(*keys: str) -> str | None:

#         for key in keys:

#             tag = (
#                 soup.find("meta", attrs={"property": key})
#                 or soup.find("meta", attrs={"name": key})
#             )

#             if tag and tag.get("content"):

#                 value = str(tag["content"]).strip()

#                 if value:
#                     return value

#         return None

#     # Extract title.
#     title = meta("og:title", "twitter:title")

#     if not title and soup.title:
#         title = soup.title.get_text(strip=True) or None

#     # Extract description.
#     description = meta(
#         "og:description",
#         "description",
#         "twitter:description",
#     )

#     # Extract preview image.
#     image = meta("og:image", "twitter:image")

#     if image:
#         image = urljoin(current_url, image)

#     # Extract website name.
#     site_name = meta("og:site_name")

#     parsed = urlparse(current_url)

#     # Extract favicon.
#     favicon_tag = soup.find(
#         "link",
#         rel=lambda value: value and "icon" in str(value).lower(),
#     )

#     favicon = (
#         urljoin(current_url, favicon_tag.get("href"))
#         if favicon_tag and favicon_tag.get("href")
#         else f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
#     )

#     # If no useful metadata is available, return fallback.
#     if not title and not description and not image and not site_name:
#         logger.warning("No useful metadata found: %s", current_url)
#         return _fallback_preview(current_url)

#     return {
#         "url": current_url,
#         "title": title or parsed.netloc,
#         "description": description or "No description is available for this website.",
#         "image_url": image,
#         "favicon_url": favicon,
#         "site_name": site_name or parsed.netloc,
#     }
