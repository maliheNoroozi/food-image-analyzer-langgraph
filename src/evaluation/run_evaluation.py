from loguru import logger
from opik import Opik

from evaluation.eval_dataset import evaluate_dataset
from evaluation.scoring import aggregate_scores

client = Opik()

if __name__ == "__main__":
    dataset_name = "Nutrition-5K"
    dataset = client.get_dataset(name=dataset_name)
    scores = evaluate_dataset(dataset=dataset)
    logger.info(scores)
    aggregated_scores = aggregate_scores(scores=scores)
    logger.info(aggregated_scores)
