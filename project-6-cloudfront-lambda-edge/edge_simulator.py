"""Local-only simulator for the CloudFront/Lambda@Edge project."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import re
from time import time
from urllib.parse import parse_qsl, urlencode

MAX_LOCAL_TOKEN_TTL_SECONDS = 900

# Intentionally illustrative patterns, not a complete WAF/security policy.
SUSPICIOUS_PATTERNS = (
    re.compile(r"<\s*script", re.IGNORECASE),
    re.compile(r"<\s*iframe", re.IGNORECASE),
    re.compile(r"union\s+select", re.IGNORECASE),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"(?:^|[/\\])\.\.(?:[/\\]|$)"),
    re.compile(r"[\r\n]"),
)


@dataclass(frozen=True)
class RequestResult:
    status_code: int
    uri: str
    reason: str
    cache_control: str | None = None


def query_is_suspicious(query_string: str) -> bool:
    try:
        parameters = parse_qsl(query_string, keep_blank_values=True, strict_parsing=False)
    except ValueError:
        return True
    for key, value in parameters:
        if any(pattern.search(key) or pattern.search(value) for pattern in SUSPICIOUS_PATTERNS):
            return True
    return False


def make_local_signature(path: str, ttl_seconds: int, secret: str, now: int | None = None) -> str:
    if not 1 <= ttl_seconds <= MAX_LOCAL_TOKEN_TTL_SECONDS:
        raise ValueError(f"ttl_seconds must be between 1 and {MAX_LOCAL_TOKEN_TTL_SECONDS}")
    issued_at = int(time()) if now is None else int(now)
    expires = issued_at + ttl_seconds
    message = f"{path}|{expires}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), message, sha256).hexdigest()
    return urlencode({"expires": str(expires), "sig": signature})


def validate_local_signature(path: str, query_string: str, secret: str, now: int | None = None) -> bool:
    params = dict(parse_qsl(query_string, keep_blank_values=True))
    expires_text = params.get("expires", "")
    supplied_signature = params.get("sig", "")
    if not expires_text.isdigit() or not supplied_signature:
        return False
    expires = int(expires_text)
    current_time = int(time()) if now is None else int(now)
    if expires <= current_time or expires > current_time + MAX_LOCAL_TOKEN_TTL_SECONDS:
        return False
    expected = hmac.new(
        secret.encode("utf-8"),
        f"{path}|{expires}".encode("utf-8"),
        sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, supplied_signature)


def cache_headers_for_path(path: str, private: bool = False) -> dict[str, str]:
    if private or path.startswith("/private/"):
        return {"Cache-Control": "private, no-store", "Vary": "Accept"}
    lower_path = path.lower()
    if lower_path.endswith((".jpg", ".jpeg", ".png", ".webp", ".avif", ".css", ".js", ".woff", ".woff2")):
        return {
            "Cache-Control": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=600",
            "Vary": "Accept",
            "X-Content-Type-Options": "nosniff",
        }
    if lower_path.endswith((".html", ".htm")) or lower_path == "/":
        return {
            "Cache-Control": "public, max-age=0, s-maxage=60, must-revalidate",
            "Vary": "Accept",
            "X-Content-Type-Options": "nosniff",
        }
    return {
        "Cache-Control": "public, max-age=300, s-maxage=1800",
        "X-Content-Type-Options": "nosniff",
    }


def inspect_request(
    uri: str,
    query_string: str = "",
    accept: str = "",
    secret: str = "local-demo-secret-change-me",
    now: int | None = None,
) -> RequestResult:
    if query_is_suspicious(query_string):
        return RequestResult(403, uri, "blocked suspicious query string", "no-store")

    if uri.startswith("/private/") and not validate_local_signature(uri, query_string, secret, now):
        return RequestResult(403, uri, "missing, expired, or invalid local access token", "no-store")

    rewritten_uri = uri
    if "image/webp" in accept.lower():
        for ext in (".jpg", ".jpeg", ".png"):
            if uri.lower().endswith(ext):
                rewritten_uri = uri[:-len(ext)] + ".webp"
                break

    return RequestResult(200, rewritten_uri, "allowed", cache_headers_for_path(rewritten_uri, private=uri.startswith("/private/")).get("Cache-Control"))


def simulate_regional_cache(requests_by_region: dict[str, list[str]], ttl_seconds: int = 60) -> dict[str, dict[str, float | int]]:
    """Deterministic virtual cache. One request advances virtual time by one second."""
    if ttl_seconds < 1:
        raise ValueError("ttl_seconds must be at least 1")
    report: dict[str, dict[str, float | int]] = {}
    for region, request_paths in requests_by_region.items():
        cache_inserted_at: dict[str, int] = {}
        hits = 0
        misses = 0
        for now, path in enumerate(request_paths):
            inserted_at = cache_inserted_at.get(path)
            if inserted_at is not None and (now - inserted_at) < ttl_seconds:
                hits += 1
            else:
                misses += 1
                cache_inserted_at[path] = now
        total = hits + misses
        report[region] = {
            "requests": total,
            "hits": hits,
            "misses": misses,
            "hit_ratio_percent": round((hits / total * 100.0), 2) if total else 0.0,
        }
    return report
