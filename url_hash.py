import base64
import hashlib


def generate_short_url_hash(long_url, length=6):
    if not isinstance(long_url, str) or not long_url.strip():
        raise ValueError("long_url must be a non-empty string")

    hash_object = hashlib.sha256(long_url.strip().encode("utf-8"))
    return base64.urlsafe_b64encode(hash_object.digest())[:length].decode("ascii")


if __name__ == "__main__":
    target_url = "https://www.youtube.com/watch?v=X-n6t2tgwEk&list=PLLa_h7BriLH2ihMfDMpSHl2PbBjSzvDtw&index=2"
    print(generate_short_url_hash(target_url))
