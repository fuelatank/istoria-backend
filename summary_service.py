from sqlalchemy.orm import Session
from models import (
    Summary,
)  # Assuming you have a Summary model defined in your models.py


def record_summary_to_db(db: Session, summary_data: dict):
    """
    Records a new summary to the database.

    Args:
        db (Session): SQLAlchemy database session.
        summary_data (dict): A dictionary containing summary details.
            Expected keys: 'history_content', 'tags', 'keywords', 'identity', 'preferences'.

    Returns:
        Summary: The newly created Summary object.
    """
    try:
        # Create a new Summary object
        new_summary = Summary(
            history_content=summary_data.get("history_content"),
            tags=summary_data.get("tags"),
            keywords=summary_data.get("keywords"),
            identity=summary_data.get("identity"),
            preferences=summary_data.get("preferences"),
        )

        # Add the new summary to the session
        db.add(new_summary)
        db.commit()
        db.refresh(new_summary)  # Refresh to get the updated object with ID

        return new_summary
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise Exception(f"Failed to record summary to database: {str(e)}")
