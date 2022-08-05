from hashlib import md5


def generate_payu_signature(signature_string: str):
    m = md5(signature_string.encode(errors="strict"))
    return m.hexdigest()
