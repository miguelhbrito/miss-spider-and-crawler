from src.models.user import User

from src.utils import parse_timestamp


class Comment:
    content = ''
    created_at = None
    author = None

    def __init__(self, comment):
        comment_content = comment.find(
            'div', {'class': 'qa-c-item-content qa-post-content'})
        if not comment_content:
            return

        self.content = comment_content.get_text().strip()

        creation_timestamp = comment.find('time')
        self.created_at = parse_timestamp(creation_timestamp['datetime'])

        user_section = comment.find('span', {'class': 'qa-c-item-who'})
        if user_section:
            self.author = User(user_section)
