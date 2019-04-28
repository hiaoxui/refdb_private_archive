import re
from abbr import abbr2full


accepted = [
        'author',
        'booktitle',
        'year',
        'title',
        # 'volume',
        'journal',
        # 'number',
]


def raw2all():

    with open('./raw.bib', 'r', encoding='utf8') as fp:
        text = fp.read()

    pub_pattern = re.compile(r'((\n|^)@.*?)(?=(\n@|$))', re.S)
    entry_pattern = re.compile(r'(?=\n).*?\},(?=\n)', re.S)
    bib_items = pub_pattern.findall(text)
    print('{} bib items found.'.format(len(bib_items)))
    all_bib_items = list()

    for bib_item in bib_items:
        content = bib_item[0]
        if content[0] == '\n':
            content = content[1:]
        first_n = content.index('\n')
        first_line = content[:first_n]
        bracket_idx = first_line.index('{')
        bib_type = first_line[1:bracket_idx]
        content = '\n' + content[first_n+1:-2] + ',\n'


        all_entries_raw = list(entry_pattern.findall(content))
        all_entries = list()
        for entry_raw in all_entries_raw:
            eq_idx = entry_raw.index(' = ')
            all_entries.append([
                entry_raw[1:eq_idx],
                entry_raw[1:-1]
            ])
        this_item = list()
        for entry_name, entry in all_entries:
            if entry_name in accepted:
                this_item.append(entry)
        item_str = first_line + '\n' + ',\n'.join(this_item) + '}'
        all_bib_items.append(item_str)
    with open('all.bib', 'w') as fp:
        fp.write('\n'.join(all_bib_items))


if __name__ == '__main__':
    raw2all()
