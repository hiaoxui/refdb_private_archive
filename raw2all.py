import re
from abbr import abbr2full


def is_last_line(line):
    return line == '}'

def is_first_line(line):
    return '@' in line and '=' not in line

def is_content(line):
    return '=' in line and '{' in line and '}' in line

accepted = [
        'author',
        # 'booktitle',
        'year',
        'title',
        'volume',
        # 'journal',
        'number',
]

def legal_content(line):
    """
    :param str line:
    :rtype: bool
    """
    for legal in accepted:
        if line.startswith(legal):
            return True
    return False


def raw2all():

    with open('./raw.bib', 'r', encoding='utf8') as fp:
        text = fp.read()

    title_pattern = re.compile('\\{(.*)\\}', re.S)

    cleaned_text = list()
    text.replace('\r\n', '\n')
    lines = text.split('\n')
    for line in lines:
        if is_first_line(line):
            cleaned_text.append(line)
        elif is_last_line(line):
            while cleaned_text[-1][-1] == ',':
                cleaned_text[-1] = cleaned_text[-1][:-1]
            cleaned_text.append(line)
            cleaned_text.append('')
        elif is_content(line):
            if legal_content(line):
                cleaned_text.append(line)
            elif line.startswith('booktitle'):
                booktitle = title_pattern.findall(line)[0]
                booktitle = abbr2full(booktitle)
                new_title = 'booktitle = {%s},' % booktitle
                cleaned_text.append(new_title)
            elif line.startswith('journal'):
                booktitle = title_pattern.findall(line)[0]
                booktitle = abbr2full(booktitle)
                new_title = 'journal = {%s},' % booktitle
                cleaned_text.append(new_title)
        else:
            if len(line) == 0:
                continue
            print(line)
            raise NotImplementedError
    all_text = '\n'.join(cleaned_text)
    with open('all.bib', 'w', encoding='utf8') as fp:
        fp.write(all_text)


if __name__ == '__main__':
    raw2all()
