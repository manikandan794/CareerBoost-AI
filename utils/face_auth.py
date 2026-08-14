"""
Server-side support for the opt-in "Face Unlock" login feature.

IMPORTANT — read before relying on this in production:

This gives returning users a *convenience* way to sign in with their
webcam instead of typing a password. It is intentionally simple and is
NOT a hardened biometric security system:

  - There is no liveness check. A clear photo or video of the person's
    face on another screen can potentially fool it (no blink/depth
    detection is performed).
  - Matching is a Euclidean-distance comparison between two 128-d
    face-api.js descriptors, computed in the browser and re-checked
    here on the server (never trust a client-reported "match: true").
  - Accuracy depends on lighting, camera quality and the browser's
    face-api.js model — false rejects (locked-out legit user) are more
    likely than false accepts if the threshold is kept conservative.

Treat it as an *additional convenience option* layered on top of a
password-based account, not a replacement for one. Never allow
Face Unlock to be the ONLY way into an account without a password
already set (a user must sign up / already have a password before
enrolling a face).
"""

import math
import time
from collections import defaultdict, deque

# In-memory per-email attempt log for simple abuse throttling.
# NOTE: this resets on process restart and is per-process (won't be
# shared across multiple gunicorn/uwsgi workers). Fine for a single-
# process student project; swap for Redis/DB-backed rate limiting
# before running this behind multiple workers in production.
_attempts = defaultdict(deque)


def euclidean_distance(a, b):
    """Straight-line distance between two equal-length numeric vectors."""
    if not a or not b or len(a) != len(b):
        return float("inf")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def is_rate_limited(email, max_attempts, window_seconds):
    """True if `email` has made >= max_attempts face-login tries in the
    last `window_seconds`. Also prunes old attempts from the log."""
    now = time.time()
    log = _attempts[email]
    while log and now - log[0] > window_seconds:
        log.popleft()
    return len(log) >= max_attempts


def record_attempt(email):
    _attempts[email].append(time.time())


def clear_attempts(email):
    _attempts.pop(email, None)


def is_valid_descriptor(descriptor, expected_length=128):
    return (
        isinstance(descriptor, list)
        and len(descriptor) == expected_length
        and all(isinstance(v, (int, float)) for v in descriptor)
    )
