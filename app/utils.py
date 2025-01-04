from nanoid import generate

def generate_poll_id():
    return generate(size=8)

def generate_admin_code():
    return generate(size=12)