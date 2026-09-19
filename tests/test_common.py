from scripts.common import norm_answer,topk_from_probs,has_image_reference

def test_norm_answer(): assert norm_answer(['D','b'])==('b','d')
def test_topk(): assert topk_from_probs({'a':.1,'b':.4,'c':.2,'d':.3,'e':0},2)==('b','d')
def test_image_dependency(): assert has_image_reference({'image_dependency':'enough text'}) is True
def test_no_image(): assert has_image_reference({'image_dependency':'none','image_paths_json':'{}'}) is False
