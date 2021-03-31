import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter


mapping = {
    'AAAI': 'Association for the Advancement of Artificial Intelligence',
    'ACL': 'Association for Computational Linguistics',
    'AI': 'Artificial Intelligence',
    'AISTATS': 'Artificial Intelligence and Statistics',
    'ASRU': 'IEEE Automatic Speech Recognition and Understanding Workshop',
    'CAV': 'Computer Aided Verification',
    'CHI': 'Conference on Human Factors in Computing Systems',
    'CLCLing': 'International Conference on Computational Linguistics and Intelligent Text Processing',
    'COLING': 'International Conference on Computational Linguistics',
    'CoNLL': 'Computational Natural Language Learning',
    'CVPR': 'Computer Vision and Pattern Recognition',
    'COLT': 'Conference on Learning Theory',
    'EACL': 'European Association for Computational Linguistics',
    'ECCV': 'European Conference on Computer Vision',
    'EMNLP': 'Empirical Methods in Natural Language Processing',
    'FOCS': 'Foundations of Computer Science',
    'HLT': 'Human Language Technology',
    'ICCV': 'IEEE International Conference on Computer Vision',
    'ICIPS': 'IEEE International Conference on Intelligent Processing Systems',
    'ICLR': 'International Conference on Learning Representations',
    'ICML': 'International Conference on Machine Learning',
    'ICRA': 'International Conference on Robotics and Automation',
    'ICSE': 'International Conference on Software Engineering',
    'ICTAI': 'IEEE International Conference on Tools with Artificial Intelligence',
    'IJCAI': 'International Joint Conference on Artificial Intelligence',
    'IJCNLP': 'International Joint Conference on Natural Language Processing',
    'ILSVRC': 'ImageNet Large Scale Visual Recognition Challenge',
    'INLG': 'International Natural Language Generation Conference',
    'IROS': 'International Conference on Intelligent Robots and Systems',
    'ISER': 'International Symposium on Experimental Robotics',
    'JAIR': 'Journal of Artificial Intelligence Research',
    'JASA': 'Journal of the American Statistical Association',
    'JMLR': 'Journal of Machine Learning Research',
    'KDD': 'International Conference on Knowledge Discovery and Data Mining',
    'LREC': 'Language Resources and Evaluation Conference',
    'MLSLP': 'Symposium on Machine Learning in Speech and Language Processing',
    'NAACL': 'North American Association for Computational Linguistics',
    'NeurIPS': 'Advances in Neural Information Processing Systems',
    'NODALIDA': 'Nordic Conference on Computational Linguistics',
    'OSDI': 'Operating Systems Design and Implementation',
    'PAMI': 'IEEE Transactions on Pattern Analysis and Machine Intelligence',
    'RECSYS': 'ACM Conference on Recommender Systems',
    'SALT': 'Semantics and Linguistic Theory',
    'SIGIR': 'ACM Special Interest Group on Information Retreival',
    'SODA': 'Symposium on Discrete Algorithms',
    'STOC': 'Symposium on Theory of Computing',
    'TACL': 'Transactions of the Association for Computational Linguistics',
    'TFS': 'IEEE Transaction on Fuzzy Systems',
    'TNN': 'IEEE Transaction on Neural Networks',
    'TOIS': 'ACM Transactions on Information Systems',
    'TSP': 'IEEE Transaction on Signal Processing',
    'UAI': 'Uncertainty in Artificial Intelligence',
    'UIST': 'User Interface Software and Technology',
    'WSDM': 'Web Search and Data Mining',
    'WWW': 'World Wide Web',
}


def abbr2full(abbr: str):
    """
    :param str abbr:
    :rtype: str
    """
    abbr = abbr.replace('{', '').replace('}', '')
    parts = abbr.split('-')
    is_abbr = [part in mapping for part in parts]
    if all(is_abbr):
        ret = ''
        for part in parts:
            ret += ' and ' + mapping[part]
        ret = ret[5:] + f' ({abbr})'
        return ret.replace('  ', ' ').strip()
    elif not is_abbr[0]:
        return abbr.replace('  ', ' ').strip()
    else:
        raise Exception(f'Unrecognized abbreviation: {abbr}')

def raw2all():

    parser = BibTexParser(common_strings=False, ignore_nonstandard_types=False)
    raw_text = open('./raw.bib', 'r', encoding='utf8').readlines()
    raw_text = '\n'.join(filter(lambda line: 'month = ' not in line, raw_text))
    bib_db = bibtexparser.loads(raw_text, parser)

    def process_entry(entry):
        if entry['ENTRYTYPE'] == 'article':
            entry['journal'] = abbr2full(entry['journaltitle'])
            del entry['journaltitle']
        if 'booktitle' in entry:
            entry['booktitle'] = abbr2full(entry['booktitle'])
        for to_remove in [
            'abstract', 'doi', 'keywords', 'file', 'address', 'annote', 'editor', 'isbn', 'issn', 'language',
            'note', 'shorttitle', 'url', 'urldate', 'eprint', 'eprinttype', 'location', 'langid', 'archiveprefix',
            'entrysubtype', 'annotation', 'editorbtype', 'eventtitle', 'editorb', 'options', 'shortjornal'
        ]:
            if to_remove in entry:
                del entry[to_remove]
        if 'date' in entry and 'year' not in entry:
            entry['year'] = entry['date'][:4]
            del entry['date']
        if entry['ENTRYTYPE'] == 'report':
            entry['ENTRYTYPE'] = 'misc'
        return entry

    bib_db.entries = list(map(process_entry, bib_db.entries))
    writer = BibTexWriter()
    writer.indent = '  '
    # writer.comma_first = True
    with open('ref.bib', 'w') as bibfile:
        bibfile.write(writer.write(bib_db))


if __name__ == '__main__':
    raw2all()
