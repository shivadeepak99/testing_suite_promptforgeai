
import pytest
from demon_engine.api.pfcl_parser import DemonEngineRouter

@pytest.fixture
def router():
    return BrainEngineRouter()

def test_chrome_chat_contract(router):
    r = router.route('chat', 'free', 'chrome', user_is_pro=False)
    assert r['output_contract'] == 'paragraphs_and_bullets'
    assert 'persona_alignment' in r['techniques']
    r = router.route('chat', 'pro', 'chrome', user_is_pro=True)
    assert r['output_contract'] == 'paragraphs_and_bullets'
    assert 'clarify_then_answer' in r['techniques']

def test_vscode_editor_contract(router):
    r = router.route('editor', 'free', 'vscode', user_is_pro=False)
    assert r['output_contract'] == 'imperative_lines'
    assert 'acceptance_criteria' in r['techniques']
    r = router.route('editor', 'pro', 'vscode', user_is_pro=True)
    assert r['output_contract'] == 'imperative_lines'
    assert 'multi_pass_refinement' in r['techniques']

def test_cursor_agent_contract(router):
    r = router.route('agent', 'pro', 'cursor', user_is_pro=True)
    assert r['output_contract'] == 'agent_plan'
    assert 'objective_expansion' in r['techniques']
    assert 'guard_infinite_loops' in r['safety']
    r = router.route('agent', 'free', 'cursor', user_is_pro=False)
    assert r['output_contract'] == 'pro_only'

def test_web_temple_contract(router):
    r = router.route('chat', 'free', 'web', user_is_pro=False)
    assert r['output_contract'] == 'marketing_friendly'
    assert 'teaser' in r['techniques'] or 'teaser' in r.get('templates', [])
    r = router.route('chat', 'pro', 'web', user_is_pro=True)
    assert r['output_contract'] == 'marketing_friendly'
    assert 'structured_outline' in r['techniques'] or 'structured_outline' in r.get('templates', [])
