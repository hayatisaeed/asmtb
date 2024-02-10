import hashlib


async def truncated_md5(input_string):
    # Convert the input string to bytes
    input_bytes = input_string.encode('utf-8')

    # Compute the MD5 hash
    md5_hash = hashlib.md5(input_bytes)

    # Get the hexadecimal representation of the hash and return the first 16 characters
    return md5_hash.hexdigest()[:16]
