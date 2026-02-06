from utils.get_post_url_id_from_post import get_post_url_id_from_post


def return_post_url_id():
    def url_id(post_id):
        return get_post_url_id_from_post(post_id)

    return dict(url_id=url_id)
