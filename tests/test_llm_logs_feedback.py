from click.testing import CliRunner


def test_plugin():
    import llm
    from llm.plugins import pm

    class MockModel(llm.Model):
        model_id = "demo"

        def __init__(self, response_text=""):
            self.response_text = response_text
            self.last_prompt = None

        def execute(self, prompt, stream, response, conversation):
            self.last_prompt = prompt
            return [self.response_text]

    mock_model = MockModel()

    class TestPlugin:
        __name__ = "TestPlugin"

        @llm.hookimpl
        def register_models(self, register):
            register(mock_model)

    pm.register(TestPlugin(), name="undo")
    try:
        from llm.cli import cli

        runner = CliRunner(mix_stderr=False)
        #TODO test mock_model.response_text = "MDL Feedback 👍"
        result = runner.invoke(
            cli,
            ["feedback+1", "nice one"],
        )
        assert result.exit_code == 0
    finally:
        pm.unregister(name="undo")