import os
import tempfile
from click.testing import CliRunner
import sqlite3

def test_plugin():
    import llm
    from llm.plugins import pm
    
    # Create a temporary database for testing
    temp_db_dir = tempfile.mkdtemp()
    temp_db_path = os.path.join(temp_db_dir, "logs.db")
    
    # Create and initialize the test database
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    
    # Create the responses table that the feedback table depends on
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id TEXT PRIMARY KEY,
            prompt TEXT,
            datetime_utc TIMESTAMP
        )
    ''')
    
    # Insert a test response
    cursor.execute('''
        INSERT INTO responses (id, prompt, datetime_utc)
        VALUES (?, ?, datetime('now'))
    ''', ('test-response-id', 'test prompt', ))
    
    conn.commit()
    conn.close()
    
    # Patch the DB_PATH
    import llm_logs_feedback
    llm_logs_feedback.DB_PATH = temp_db_path

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
        mock_model.response_text = "MDL Feedback 👍"
        result = runner.invoke(
            cli,
            ["feedback+1", "nice one"],
        )
        assert result.exit_code == 0
        
        # Verify the feedback was stored
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT feedback, comment FROM feedback LIMIT 1')
        feedback_row = cursor.fetchone()
        conn.close()
        
        assert feedback_row is not None
        assert feedback_row[0] == '+1'
        assert feedback_row[1] == 'nice one'
        
    finally:
        pm.unregister(name="undo")
        # Clean up the temporary database
        os.remove(temp_db_path)
        os.rmdir(temp_db_dir)