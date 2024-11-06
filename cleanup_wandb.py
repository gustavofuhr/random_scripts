import wandb
import os
from datetime import timedelta

def cleanup_wandb_runs(project_name, entity_name, duration_threshold_minutes=1, dry_run=True):
    """
    Deletes W&B runs that either failed or finished quickly.

    Args:
        project_name (str): Name of the W&B project.
        entity_name (str): Name of the W&B entity.
        duration_threshold_minutes (int): Duration threshold in minutes to determine short runs.
        dry_run (bool): If True, no runs are deleted, only printed.
    """
    # Initialize W&B API
    wandb.login(key=os.getenv("WANDB_API_KEY"))
    api = wandb.Api()

    # Verify if the project exists before proceeding
    try:
        projects = api.projects(entity=entity_name)
        print(f"Projects available under entity '{entity_name}':")
        for project in projects:
            print(f" - {project.name}")
        project = next(proj for proj in projects if proj.name == project_name)
        print(f"Found project: {project.name}")
    except StopIteration:
        raise ValueError(f"Could not find project '{project_name}' under entity '{entity_name}'. Ensure the project is accessible.")

    # Set your duration threshold as a timedelta object
    duration_threshold = timedelta(minutes=duration_threshold_minutes)

    # Fetch all runs in the project
    try:
        runs = api.runs(f"{entity_name}/{project_name}")
        print(f"Found {len(runs)} runs in the project '{project_name}'.")
    except wandb.errors.CommError as e:
        raise RuntimeError(f"Error fetching runs: {e}")

    for run in runs:
        # Calculate run duration (or skip runs that aren't finished or running)
        if run.state == "finished" and run.summary.get('_runtime'):
            duration_seconds = run.summary.get('_runtime')
            if duration_seconds < duration_threshold.total_seconds():
                print(f"[DRY RUN] Deleting short run {run.name} (ID: {run.id}, Duration: {duration_seconds} seconds)")
                if not dry_run:
                    run.delete()
                    print(f"Run {run.name} deleted successfully.")
        elif run.state == "failed":
            # Delete failed runs
            print(f"[DRY RUN] Deleting failed run {run.name} (ID: {run.id})")
            if not dry_run:
                run.delete()
                print(f"Run {run.name} deleted successfully.")

# Example usage
cleanup_wandb_runs(
    project_name="mmdetection-upps",
    entity_name="gfuhr2",
    duration_threshold_minutes=1,
    dry_run=False  # Set to False to perform actual deletion
)
