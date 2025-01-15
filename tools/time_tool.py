from datetime import datetime
from langchain_core.tools import StructuredTool
from pydantic import BaseModel


def get_current_time():
    """Returns the current time in HH:MM AM/PM format."""
    now = datetime.now()
    return now.strftime("%I:%M %p")


class TimeToolArgsSchema(BaseModel):
    """Schema for the arguments of the time tool."""

    # No arguments needed since this tool just returns the current time
    pass


time_tool = StructuredTool(
    name="Time",
    description="Returns the current time in HH:MM AM/PM format.",
    func=get_current_time,
    args_schema=TimeToolArgsSchema,
)
