from datetime import datetime
from langchain_core.tools import StructuredTool
from pydantic import BaseModel


def get_current_datetime():
    """Returns the current date and time in YYYY-MM-DD HH:MM:SS AM/PM format."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %I:%M:%S %p")


class DateTimeToolArgsSchema(BaseModel):
    """Schema for the arguments of the datetime tool."""

    # No arguments needed since this tool just returns the current datetime
    pass


datetime_tool = StructuredTool(
    name="DateTime",
    description="Returns the current date and time in YYYY-MM-DD HH:MM:SS AM/PM format.",
    func=get_current_datetime,
    args_schema=DateTimeToolArgsSchema,
)
