from flask_webb.models import bibs

#Want to check bibliography info is stored correctly! 
def test_bib():
    bb = bibs('test_reftag', 'test_author_list', 'test', 0, 'test', 0, 'test', 'test')
    assert bb.ref_tag =='test_reftag'
    assert bb.volume == 0
    assert bb.author_list == 'test_author_list' 
