class User:
    name = None
    title = None
    score = None

    def __init__(self, user_section):
        section_type = user_section.find('span')['class'][0].split('-')
        section_type = '-'.join(section_type[1:3])

        self.name = user_section.find('span', {'itemprop': 'name'}).text

        if self.name == 'anónimo':
            self.name = 'Anônimo'
            return

        try:
            self.title = user_section.find(
                'span', {'class': 'qa-{}-who-title'.format(section_type)}).text
        except AttributeError:
            pass

        try:
            score = user_section.find(
                'span', {'class': 'qa-{}-who-points-data'.format(section_type)}).text
            if 'k' in score:
                score = int(score.replace('k', '').replace('.', '')) * 100
            self.score = score
        except AttributeError:
            pass
