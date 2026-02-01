import logging
import os
import random
from pathlib import Path

import yaml
from dotenv import load_dotenv

from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TextPart
from a2a.utils import get_message_text


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("videoindex_qa")

QA_DATA_DIR = os.getenv("QA_DATA_DIR", "data")


def load_qa_data(data_dir: str) -> list[dict]:
    """Load all Q&A YAML files from the data directory."""
    qa_data = []
    data_path = Path(data_dir)
    if not data_path.exists():
        logger.warning(f"Data directory does not exist: {data_dir}")
        return qa_data
    for yaml_file in data_path.glob("*.yaml"):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and "questions" in data:
                    num_questions = len(data["questions"])
                    qa_data.extend(data["questions"])
                    logger.info(f"Loaded {num_questions} questions from {yaml_file.name}")
        except Exception as e:
            logger.error(f"Failed to load {yaml_file.name}: {e}")
    logger.info(f"Total questions loaded: {len(qa_data)}")
    return qa_data


def find_answer(question: str, qa_data: list[dict]) -> tuple[str | None, str | None]:
    """Search for a matching question and return a random answer option."""
    question_lower = question.lower().strip()
    for qa in qa_data:
        if qa.get("question", "").lower().strip() == question_lower:
            options = qa.get("options", {})
            if options:
                # Randomly select one of the answer options
                answer_key = random.choice(list(options.keys()))
                answer = options[answer_key]
                return answer, answer_key
    return None, None


class Agent:
    def __init__(self):
        self.qa_data = load_qa_data(QA_DATA_DIR)

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        question = get_message_text(message)
        logger.info(f"Received question: {question[:100]}...")

        answer, answer_key = find_answer(question, self.qa_data)

        if answer:
            logger.info(f"Found question, returning random answer: {answer_key}")
        else:
            logger.warning("Question not found in dataset")
            answer = "Question not found in the video Q&A dataset."

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=answer))],
            name="Answer",
        )
