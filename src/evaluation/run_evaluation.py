from opik import Opik
from dotenv import find_dotenv, load_dotenv
from loguru import logger

from evaluation.eval_dataset import evaluate_dataset
from evaluation.scoring import aggregate_scores

load_dotenv(find_dotenv())
client = Opik()

if __name__ == "__main__":
    dataset_name = "Nutrition-5K"
    dataset = client.get_dataset(name=dataset_name)
    scores = evaluate_dataset(dataset=dataset)
    aggregated_scores = aggregate_scores(scores=scores)
    logger.info(aggregated_scores)
