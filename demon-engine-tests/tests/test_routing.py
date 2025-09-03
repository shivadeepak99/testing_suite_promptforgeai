
import pytest
from demon_engine.api.pfcl_parser import DemonEngineRouter
from demon_engine.services.brain_engine.errors import ProRequiredError, KillSwitchError, PipelineNotFound

@pytest.fixture
def router():
    return BrainEngineRouter()

def test_exact_hit(router):
    r = router.route('chat', 'free', 'chrome', user_is_pro=False)
    assert r['matched_pipeline'] == 'Conversational.Basic'
    r = router.route('editor', 'pro', 'vscode', user_is_pro=True)
    assert r['matched_pipeline'] == 'CodeForge.LangGraph'

def test_wildcard_fallback(router):
    r = router.route('chat', 'free', 'unknown', user_is_pro=False)
    assert r['matched_pipeline'] == 'Conversational.Basic'

def test_pro_gating(router):
    with pytest.raises(ProRequiredError):
        router.route('agent', 'pro', 'cursor', user_is_pro=False)

def test_killswitch(router):
    # Enable kill switch for a key
    key = ('chat', 'free', 'chrome')
    router.features.enable_killswitch(key)
    with pytest.raises(KillSwitchError):
        router.route('chat', 'free', 'chrome', user_is_pro=False)
    # Other keys still work
    r = router.route('chat', 'free', 'web', user_is_pro=False)
    assert r['matched_pipeline'] == 'Temple.Basic'

def test_backward_compatibility(router):
    # No intent/client: should infer chat/free/*
    r = router.route(None, None, None, user_is_pro=False)
    assert r['matched_pipeline'] == 'Conversational.Basic'

def test_pipeline_not_found(router):
    # Remove all fallbacks
    router.registry._matrix.clear()
    with pytest.raises(PipelineNotFound):
        router.route('chat', 'free', 'chrome', user_is_pro=False)
