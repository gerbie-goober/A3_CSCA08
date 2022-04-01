"""CSC108/A08: Fall 2021 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Anya Tafliovich.

"""

import copy  # needed in examples of functions that modify input dict
from typing import Dict, List, TextIO

# remove unused constants from this import statement when you are
# finished with your assignment
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS,
                       ABSTRACT, END, SEPARATOR, NameType,
                       ArticleValueType, ArticleType, ArxivType)


EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

arxiv_copy = {'008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to\n
Computer Science is the best course.'''}, '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of\n
Toronto is the best university.'''}}

EXAMPLE_BY_AUTHOR = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031'],
    ('Pancer', 'Richard'): ['067']
}



# We provide this PARTIAL docstring to show the use of examples.
def make_author_to_articles(id_to_article: ArxivType) -> Dict[NameType,
                                                              List[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> make_author_to_articles(arxiv_copy) == {
    ... ('Ponce', 'Marcelo'): ['008', '827'],
    ... ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ... ('Bretscher', 'Anna'): ['827']}
    True
    """
    author_to_articles = {}
    make_author_key(author_to_articles, id_to_article)
    add_ids_to_authors(author_to_articles, id_to_article)
    for authors in author_to_articles:
        author_to_articles[authors].sort()
    return author_to_articles

def make_author_key(author_to_articles: Dict[NameType, List[str]],
                    id_to_article: ArxivType) -> None:
    """Return a dict that makes each author name found in id_to_article
    a key in the dictionary.

    >>> temp = {}
    >>> make_author_key(temp, EXAMPLE_ARXIV)
    >>> temp == {('Ponce', 'Marcelo'): None,
    ... ('Tafliovich', 'Anya Y.'): None,
    ... ('Bretscher', 'Anna'): None,
    ... ('Breuss', 'Nataliya'): None,
    ... ('Pancer', 'Richard'): None}
    True
    >>> temp = {}
    >>> make_author_key(temp, arxiv_copy)
    >>> temp == {('Ponce', 'Marcelo'): None,
    ... ('Tafliovich', 'Anya Y.'): None,
    ... ('Bretscher', 'Anna'): None}
    True

    """
    for key in id_to_article:
        for author in id_to_article[key][AUTHORS]:
            if author not in author_to_articles:
                author_to_articles[author] = None

def add_ids_to_authors(author_to_articles: Dict[NameType, List[str]],
                       id_to_article: ArxivType) -> None:
    """Modify dict author_to_articles to contain the ids as the values
    corresponding to the key in the dict.

    >>> temp = {('Ponce', 'Marcelo'): None,
    ... ('Tafliovich', 'Anya Y.'): None,
    ... ('Bretscher', 'Anna'): None,
    ... ('Breuss', 'Nataliya'): None,
    ... ('Pancer', 'Richard'): None}
    >>> add_ids_to_authors(temp, EXAMPLE_ARXIV)
    >>> temp == EXAMPLE_BY_AUTHOR
    True
    >>> temp = {('Ponce', 'Marcelo'): None,
    ... ('Tafliovich', 'Anya Y.'): None,
    ... ('Bretscher', 'Anna'): None}
    >>> add_ids_to_authors(temp, arxiv_copy)
    >>> temp ==  {('Ponce', 'Marcelo'): ['008', '827'],
    ... ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ... ('Bretscher', 'Anna'): ['827']}
    True
    """
    for ids in id_to_article:
        for author in id_to_article[ids][AUTHORS]:
            if author_to_articles[author] is None:
                author_to_articles[author] = [ids]
            else:
                author_to_articles[author].append(ids)

def get_coauthors(id_to_article: ArxivType, author: NameType) -> List[NameType]:
    """Return a list of coauthors (sorted in lexographic order) of the author
    specified by the author author.

    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.')) == [(
    ... 'Bretscher', 'Anna'), ('Ponce', 'Marcelo')]
    True
    >>> get_coauthors(arxiv_copy, ('Bretscher', 'Anna')) == [
    ... ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    True
    """
    coauthor_lst = []
    for ids in id_to_article:
        temp = id_to_article[ids][AUTHORS]
        for i in temp:
            if author not in temp:
                break
            if i not in coauthor_lst and i != author:
                coauthor_lst.append(i)
    coauthor_lst.sort()
    return coauthor_lst

def get_most_published_authors(id_to_article: ArxivType) -> List[NameType]:
    """Return a list of authors (sorted in lexographic order) who published the
    most articles. In the case of a tie, the list should have more
    than one author.

    >>> get_most_published_authors(EXAMPLE_ARXIV) == [('Bretscher', 'Anna'),
    ... ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    True
    >>> expected = [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> expected == get_most_published_authors(arxiv_copy)
    True

    """
    temp = {}
    most_published_list = []
    make_author_key(temp, id_to_article)
    add_count_to_authors(temp, id_to_article)
    for key in temp:
        if temp[key] == max(list(temp.values())):
            most_published_list.append(key)
    most_published_list.sort()
    return most_published_list

def add_count_to_authors(author_to_articles: Dict[NameType, List],
                         id_to_article: ArxivType) -> None:
    """Modify dict author_to_articles to contain the number of articles
    as the values corresponding to the key (author) in the dict.

    >>> temp = {('Ponce', 'Marcelo'): None,
    ... ('Tafliovich', 'Anya Y.'): None,
    ... ('Bretscher', 'Anna'): None,
    ... ('Breuss', 'Nataliya'): None,
    ... ('Pancer', 'Richard'): None}
    >>> add_count_to_authors(temp, EXAMPLE_ARXIV)
    >>> expected = {('Ponce', 'Marcelo'): 2, ('Tafliovich', 'Anya Y.'): 2,
    ... ('Breuss', 'Nataliya'): 1, ('Bretscher', 'Anna'): 2,
    ... ('Pancer', 'Richard'): 1}
    >>> temp == expected
    True
    >>> temp = {('Ponce', 'Marcelo'): None,
    ... ('Tafliovich', 'Anya Y.'): None,
    ... ('Bretscher', 'Anna'): None}
    >>> add_count_to_authors(temp, arxiv_copy)
    >>> expected = {('Ponce', 'Marcelo'): 2, ('Tafliovich', 'Anya Y.'): 2,
    ... ('Bretscher', 'Anna'): 1}
    >>> temp == expected
    True

    """
    for ids in id_to_article:
        for authors in id_to_article[ids][AUTHORS]:
            if author_to_articles[authors] is None:
                author_to_articles[authors] = 1
            else:
                author_to_articles[authors] += 1

def suggest_collaborators(id_to_article: ArxivType,
                          author: NameType) -> List[NameType]:
    """Return a list of authors (sorted in lexicographic order) with whom the
    author specified by the author author, who is encouraged to collaborate.

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Pancer', 'Richard'))
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Pancer', 'Richard')]

    """
    coauthor_list = get_coauthors(id_to_article, author)
    collab_lst = []
    for coauthor in coauthor_list:
        temp = get_coauthors(id_to_article, coauthor)
        for coll in temp:
            if coll != author and coll not in (collab_lst and coauthor_list):
                collab_lst.append(coll)
    collab_lst.sort()
    return collab_lst

def has_prolific_authors(author_to_ids: Dict[NameType, List[str]],
                         article: ArticleType, min_publications: int) -> bool:
    """Return True if and only if the article article has at least one author
    who has published at least min_publications papers.

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['008'], 2)
    True

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['031'], 2)
    False

    """
    count = 0
    for ids in list(author_to_ids.values()):
        for ide in ids:
            if ide == article[ID] and len(ids) >= min_publications:
                count += 1
    return count >= 1

# We provide this PARTIAL docstring to show use of copy.deepcopy.
def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update id_to_article so that it contains only articles published by
    authors with min_publications or more articles published. As long
    as at least one of the authors has min_publications, the article
    is kept.

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '008' in arxiv_copy and '067' in arxiv_copy and '827' in arxiv_copy
    True

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 3)
    >>> len(arxiv_copy)
    0
    >>> '827' in arxiv_copy
    False
    """
    temp = make_author_to_articles(id_to_article)
    articles_to_remove = []
    for ids in id_to_article:
        if not has_prolific_authors(temp, id_to_article[ids], min_publications):
            articles_to_remove.append(ids)
    for article in articles_to_remove:
        id_to_article.pop(article)

# Note that we do not include example calls since the function works
# on an input file.
def read_arxiv_file(afile: TextIO) -> ArxivType:
    """Return a dict containing all arxiv information in afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout
    """
    id_to_article = {}
    line = afile.readline()
    while line != '':
        temp = {}
        #in the temp, store the id of the article
        temp[ID] = line.strip('\n')
        line = afile.readline()
        #store the title of the article
        temp[TITLE] = None
        if line != '\n':
            temp[TITLE] = line.strip('\n')
        line = afile.readline()
        #store the created date of the article
        temp[CREATED] = None
        if line != '\n':
            temp[CREATED] = line.strip('\n')
        line = afile.readline()
        #store the modified date of the article
        temp[MODIFIED] = None
        if line != '\n':
            temp[MODIFIED] = line.strip('\n')
        #store the authors of the article
        add_authors(temp, afile)
        #store the abstract of the article
        add_abstract(temp, afile)
        #add temp dict to id_to_article
        id_to_article[temp[ID]] = temp
        #read the next line after END
        line = afile.readline()
    return id_to_article

def add_authors(temp: Dict[str, None], afile: TextIO) -> None:
    """Modify dic temp to contain authors in tuple format (in lexicographic
    order) from the file afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout
    """
    line = afile.readline()
    temp[AUTHORS] = []
    if line != '\n':
        while line != '\n':
            name = line.strip('\n')
            temp[AUTHORS].append(tuple(name.split(SEPARATOR)))
            line = afile.readline()
        temp[AUTHORS].sort()

def add_abstract(temp: Dict[str, None], afile: TextIO) -> None:
    """Modify dic temp to contain the abstract from the file afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout
    """
    line = afile.readline()
    temp[ABSTRACT] = None
    if line != '\n':
        temp[ABSTRACT] = ''
        while line != END + '\n':
            temp[ABSTRACT] += line
            line = afile.readline()
        temp[ABSTRACT] = temp[ABSTRACT].rstrip('\n')

if __name__ == '__main__':

    import doctest
    doctest.testmod()

    with open('example_data.txt') as example_data:
        example_arxiv = read_arxiv_file(example_data)
        print('Did we produce a correct dict? ',
              example_arxiv == EXAMPLE_ARXIV)

    ##uncomment to work with a larger data set
    #with open('data.txt') as data:
       #arxiv = read_arxiv_file(data)

    #author_to_articles = make_author_to_articles(arxiv)
    #most_published = get_most_published_authors(arxiv)
    #print(most_published)
    #print(get_coauthors(arxiv, ('Varanasi', 'Mahesh K.')))  # one
    #print(get_coauthors(arxiv, ('Chablat', 'Damien')))  # many
