import click
from loguru import logger
from experiment.bin.logger import bind_context_to_logger
from experiment.utils.s3_utils import upload_to_s3


@click.command(name="scan")
@click.option("--target", "target", type=str, help="The website to target.", required=True)
@click.option("--scan-id", "scan_id", type=str, help="The scan ID to use.", required=True)
# @click.pass_context  # Pass the context into the command function
# def scan(ctx, target, scan_id):
def scan(target, scan_id):
    # Access environment_name from the context
    logger.info(f"Scanning {target}")
    upload_to_s3()
    bind_context_to_logger(scan_id=scan_id)
    logger.info("Scanning the target")

