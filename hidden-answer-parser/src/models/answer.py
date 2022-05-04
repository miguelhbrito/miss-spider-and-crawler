from src.models.comment import Comment
from src.models.user import User

from src.utils import parse_timestamp


class Answer:
    up_votes = 0
    down_votes = 0
    content = ''
    created_at = None
    user = None
    comments = []

    def __init__(self, answer_section):
        votes_section = answer_section.find(
            'div', {'class': 'qa-voting qa-voting-updown'})
        self.up_votes = int(votes_section.find(
            'span', {'class': 'qa-upvote-count-data'}).text)
        self.down_votes = int(votes_section.find(
            'span', {'class': 'qa-downvote-count-data'}).text)

        content = answer_section.find(
            'div', {'class': 'qa-a-item-content qa-post-content'})
        self.content = content.get_text().strip()

        answered_time_section = answer_section.find(
            'span', {'class': 'qa-a-item-when-data'})
        self.created_at = parse_timestamp(
            answered_time_section.find('time')['datetime'])

        user_section = answer_section.find('span', {'class': 'qa-a-item-who'})
        self.user = User(user_section)

        comments_section = answer_section.find(
            'div', {'class': 'qa-a-item-c-list'})
        self.comments = self._parse_comments(comments_section)

    def _parse_comments(self, comments_section):
        all_comment_items = comments_section.findAll(
            'div', {'class': 'qa-c-list-item'})

        comments = []
        for comment_item in all_comment_items:
            comments.append(Comment(comment_item))

        return comments
