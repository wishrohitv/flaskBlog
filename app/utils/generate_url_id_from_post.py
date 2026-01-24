import uuid

from models import Post


def check_if_url_id_exists_in_post_db(url_id):
    return Post.query.filter_by(url_id=url_id).first() is not None


AVOID_CHARACTERS = [
    " ",
    "<",
    ">",
    "#",
    "%",
    "{",
    "}",
    "|",
    "\\",
    "^",
    "~",
    "[",
    "]",
    "`",
    '"',
    "'",
    ":",
    ";",
    "/",
    "?",
    "=",
    "&",
    "@",
    "+",
    ".",
    ",",
]


def get_new_uid():
    return str(uuid.uuid4())[24:]


def get_slug_from_post_title(post_title):
    cleaned_title = "".join(
        ["-" if char in AVOID_CHARACTERS else char for char in post_title]
    )
    filtered_words = [word for word in cleaned_title.split("-") if word]
    final_url = "-".join(filtered_words)
    return f"{final_url}".lower()


def generate_url_id():
    new_url_id = get_new_uid()
    counter = 1

    while check_if_url_id_exists_in_post_db(new_url_id):
        new_url_id = f"{new_url_id}{counter}"
        counter += 1

    return new_url_id
