from src.models.answer import Answer
from src.models.comment import Comment
from src.models.user import User

from src.utils import parse_timestamp


class Question:
    up_votes = 0
    down_votes = 0
    title = ''
    content = ''
    tags = []
    category = ''
    author = None
    created_at = None
    best_answer = None
    comments = []
    answers = []

    def __init__(self, parsed_html):
        self.title = parsed_html.title.text.split(' - Respostas Ocultas')[0]

        question_section = parsed_html.find(
            'div', {'class': 'qa-q-view'})

        content = question_section.find(
            'div', {'class': 'qa-q-view-content qa-post-content'})
        self.content = content.get_text().strip()

        vote_section = question_section.find(
            'div', {'class': 'qa-q-view-stats'})

        self.up_votes = int(vote_section.find(
            'span', {'class': 'qa-upvote-count-data'}).text)

        self.down_votes = int(vote_section.find(
            'span', {'class': 'qa-downvote-count-data'}).text)

        tags_list = question_section.find(
            'ul', {'class': 'qa-q-view-tag-list'})
        if tags_list:
            self.tags = [tag.text for tag in tags_list.findAll('li')]
        else:
            self.tags = []

        try:
            question_info = question_section.find(
                'span', {'class': 'qa-q-view-avatar-meta'})

            creation_timestamp = question_info.find('time')
            self.created_at = parse_timestamp(creation_timestamp['datetime'])
            self.category = question_info.find(
                'a', {'class': 'qa-category-link'}).text

            user_section = question_section.find(
                'span', {'class': 'qa-q-view-who'})
            self.author = User(user_section)

            comments_section = question_section.find(
                'div', {'class': 'qa-q-view-c-list'})
            self.comments = self._parse_comments(comments_section)

            answers_section = parsed_html.find('div', {'class': 'qa-a-list'})
            self._parse_answers(answers_section)
        except AttributeError as e:
            print(self.tags)
            raise e

    def _parse_comments(self, comments_section):
        all_comment_items = comments_section.findAll(
            'div', {'class': 'qa-c-list-item'})

        comments = []
        for comment_item in all_comment_items:
            comments.append(Comment(comment_item))

        return comments

    def _parse_answers(self, answers_section):
        best_answer = answers_section.find(
            'div', {'class': 'qa-a-list-item qa-a-list-item-selected'})
        if best_answer:
            self.best_answer = Answer(best_answer)

        regular_answer_items = answers_section.findAll(
            'div', {'class': 'qa-a-list-item'})

        answers = []
        for answer_item in regular_answer_items:
            answers.append(Answer(answer_item))
        self.answers = answers
