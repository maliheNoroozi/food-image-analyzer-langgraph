from dotenv import find_dotenv, load_dotenv
from langsmith import Client as LangSmithClient
from loguru import logger

from evaluation.eval_dataset import evaluate_dataset
from evaluation.scoring import aggregate_scores

load_dotenv(find_dotenv())
client = LangSmithClient()

if __name__ == "__main__":
    dataset_name = "food-image-analyzer"
    dataset = client.read_dataset(dataset_name=dataset_name)
    scores = evaluate_dataset(client=client, dataset=dataset)
    aggregated_scores = aggregate_scores(scores=scores)
    logger.info({"aggregated_scores": aggregated_scores})
