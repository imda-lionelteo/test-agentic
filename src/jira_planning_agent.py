import asyncio
from dataclasses import field
from enum import Enum
from typing import Optional, Union

from agents import Agent, Runner, TResponseInputItem
from pydantic import BaseModel

from src.agents_tools import web_search_tool
from src.data_structures import Feedback


# Jira Structured Data
class TaskStatus(Enum):
    """
    Enum representing the possible states of a task.

    Attributes:
        TODO (str): Task has not been started yet.
        IN_PROGRESS (str): Task is currently being worked on.
        DONE (str): Task has been completed.
    """

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Priority(Enum):
    """
    Enum representing the priority levels for tasks.

    Attributes:
        CRITICAL (str): Indicates the highest priority level.
        HIGH (str): Indicates a high priority level.
        MEDIUM (str): Indicates a medium priority level.
        LOW (str): Indicates a low priority level.
    """

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class StoryPoints(Enum):
    """
    Enum representing Fibonacci-style story point values for estimating task complexity.

    Attributes:
        XS (int): Extra small complexity, value 1.
        S (int): Small complexity, value 2.
        M (int): Medium complexity, value 3.
        L (int): Large complexity, value 5.
        XL (int): Extra large complexity, value 8.
        XXL (int): Double extra large complexity, value 13.
        UNDEFINED (int): Undefined complexity, value 0.
    """

    XS = 1
    S = 2
    M = 3
    L = 5
    XL = 8
    XXL = 13
    UNDEFINED = 0


class Task(BaseModel):
    """
    Represents a single task or work item that is part of a project.

    Attributes:
        task_id (str): Unique identifier for the task.
        name (str): Name of the task.
        description (str): Detailed description of what needs to be done.
        status (TaskStatus): Current status of the task, default is TaskStatus.TODO.
        priority (Priority): Priority level of the task, default is Priority.MEDIUM.
        acceptance_criteria (list[str]): List of criteria that must be met for the task to be considered complete.
        technical_notes (list[str]): List of technical notes or implementation details.
        assignee (Optional[str]): Team member assigned to the task, default is None.
        estimated_hours (Optional[float]): Estimated time required to complete the task, default is None.
        linked_issues (list[str]): List of tasks that are linked to this task.
    """

    task_id: str  # Unique identifier for the task
    name: str  # Name of the task
    description: str  # Detailed description of what needs to be done
    status: TaskStatus = (
        TaskStatus.TODO
    )  # Current status of the task, default is TaskStatus.TODO
    priority: Priority = (
        Priority.MEDIUM
    )  # Priority level of the task, default is Priority.MEDIUM
    acceptance_criteria: list[str] = field(
        default_factory=list
    )  # List of criteria for task completion
    technical_notes: list[str] = field(
        default_factory=list
    )  # List of technical notes or implementation details
    assignee: Optional[str] = None  # Team member assigned to the task, default is None
    estimated_hours: Optional[float] = (
        None  # Estimated time required to complete the task, default is None
    )
    linked_issues: list[str] = field(
        default_factory=list
    )  # List of tasks that are linked to this task


class Story(BaseModel):
    """
    Represents a user story that delivers business value.

    Attributes:
        story_id (str): Unique identifier for the story.
        name (str): Name of the story.
        description (str): Detailed description of what needs to be done.
        status (TaskStatus): Current status of the story, default is TaskStatus.TODO.
        priority (Priority): Priority level of the story, default is Priority.MEDIUM.
        acceptance_criteria (list[str]): List of criteria that must be met for the story to be considered complete.
        technical_notes (list[str]): List of technical notes or implementation details.
        assignee (Optional[str]): Team member assigned to the story, default is None.
        estimated_hours (Optional[float]): Estimated time required to complete the story, default is None.
        linked_issues (list[str]): List of tasks that are linked to this story.
    """

    story_id: str  # Unique identifier for the story
    name: str  # Name of the story
    description: str  # Detailed description of what needs to be done
    status: TaskStatus = (
        TaskStatus.TODO
    )  # Current status of the story, default is TaskStatus.TODO
    priority: Priority = (
        Priority.MEDIUM
    )  # Priority level of the story, default is Priority.MEDIUM
    acceptance_criteria: list[str] = field(
        default_factory=list
    )  # List of criteria for story completion
    technical_notes: list[str] = field(
        default_factory=list
    )  # List of technical notes or implementation details
    assignee: Optional[str] = None  # Team member assigned to the story, default is None
    estimated_hours: Optional[float] = (
        None  # Estimated time required to complete the story, default is None
    )
    linked_issues: list[str] = field(
        default_factory=list
    )  # List of tasks that are linked to this story


class Epic(BaseModel):
    """
    Represents a significant body of work that can be divided into multiple stories or tasks.

    Attributes:
        id (str): Unique identifier for the epic.
        name (str): Name of the epic.
        description (str): High-level overview of the feature or theme.
        priority (Priority): Priority level of the epic, default is Priority.MEDIUM.
        child_issues (list[Union[Task, Story]]): List of child tasks or stories associated with the epic.

    Example:
        epic = Epic(
            id="EPIC-1",
            name="User Authentication System",
            description="Implementation of user authentication system",
            priority=Priority.HIGH,
            child_issues=[task1, story1]
        )
    """

    id: str  # Unique identifier for the epic
    name: str  # Name of the epic
    description: str  # High-level overview of the feature or theme
    priority: Priority = (
        Priority.MEDIUM
    )  # Priority level of the epic, default is Priority.MEDIUM
    child_issues: list[Union[Task, Story]] = field(
        default_factory=list
    )  # List of child tasks or stories associated with the epic


class JiraContext(BaseModel):
    """
    Represents the top-level container for all project planning information.

    Attributes:
        epics (list[Epic]): A list of major features or themes.

    Example:
        requirements = JiraContext(
            epics=[epic1, epic2]
        )
    """

    epics: list[Epic]  # A list of major features or themes


class JiraPlanningResult(BaseModel):
    """
    Represents the outcome of the Jira planning process.

    Attributes:
        creation_timestamp (str): The timestamp indicating when the planning result was generated.
        jira_thought_instructions (str): The instructions and insights derived during the Jira planning process.
    """

    creation_timestamp: (
        str  # The timestamp indicating when the planning result was generated
    )
    jira_thought_instructions: (
        str  # The instructions and insights derived during the Jira planning process
    )


# Jira Agents
jira_planning_agent = Agent(
    name="Jira Planning Agent",
    model="o3-mini",
    instructions="""
    You are an expert in product and project management.
    Your primary responsibility is to break down the provided document and analyze all epics, stories, 
    and tasks to create a structured Jira plan.

    Your Responsibilities
    1. Extract and Populate
    - The user will provide a document containing project details, epics, stories, and tasks.
    - Your first responsibility is to extract all epics, stories, and tasks from the document and ensure no epic 
    is skipped.

    2. Enhance and Expand Where Necessary
    - If the provided document lacks certain epics, stories, or tasks, you must create them based on your expertise.
    - Ensure that the final project plan is comprehensive and enables subsequent agents to design and implement
    the project effectively.

    3. Think through what is provided and what is not provided
    - There must be epics, and stories within epics, and tasks within stories.
    
    4. Output
    - Your output will be a list of JiraPlanningResult instances where each planning result contains information
    about a single epic with its associated stories and tasks.
    """,
    output_type=list[JiraPlanningResult],
)

jira_epic_gen_agent = Agent(
    name="Jira Generation Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in products and JIRA.

    The previous agent has provided a thought instruction for an epic with its associated stories and tasks for Jira.
    Your task is to follow these instructions strictly.

    1. Familiarize Yourself with JIRA
    Before proceeding, use the WebSearchTool to search for and digest the following resources:
    - Jira Documentation: [https://support.atlassian.com/jira-software-cloud/docs/](https://support.atlassian.com/jira-software-cloud/docs/)
    - Jira Epics, Stories, and Tasks: [https://www.atlassian.com/agile/project-management/epics-stories-themes/](https://www.atlassian.com/agile/project-management/epics-stories-themes/)

    Ensure you fully understand JIRA structure and conventions before creating Epic.
    If any field is unclear, consult these sources before proceeding.

    2. Populate Epic Instance
    Ensure that all required fields are populated with relevant values.

    You must create a Epic instance with stories and tasks instances with its information.
    Strictly follow these steps and ensure a high-quality, complete Jira project breakdown.
    """,
    tools=[web_search_tool],
    output_type=Epic,
)

jira_consistency_check_agent = Agent(
    name="Jira Consistency Check Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in products and JIRA.

    You are provided with:
    - The original document containing project information.
    - The thought instructions of each epic.
    - The epic instances that contains associated stories and tasks.

    Your role is to analyze and validate the epic instance, ensuring that the epic, stories, and tasks:
    1. Are consistent with the original document and its respective thought instructions.
    2. Are consistent with the different epic instances.
    3. Are properly linked to each other.
    4. Follow the correct data structure of Epic and are not just unstructured text.

    Before validation, use the WebSearchTool to retrieve and review:
    - Jira Documentation: [https://support.atlassian.com/jira-software-cloud/docs/](https://support.atlassian.com/jira-software-cloud/docs/)
    - Jira Epics, Stories, and Tasks: [https://www.atlassian.com/agile/project-management/epics-stories-themes/](https://www.atlassian.com/agile/project-management/epics-stories-themes/)

    Ensure you understand Jira's structure and best practices before performing any validation.

    Your analysis must check the following:

    1. Consistency with Thought Instructions
    - Verify that epic, stories, and tasks in Epic match the provided thought instruction.
    - Ensure no required elements are missing or incorrectly added.

    2. Consistency with Different Epics
    - Ensure that the epic, stories, and tasks are consistent with the different epic instances.

    3. Completeness and Proper Linkage
    - Ensure that every story belongs to an epic and every task is linked to a story when applicable.
    - Verify that dependencies are correctly linked between related issues.

    4. Structural Compliance with Epic Format
    - Ensure the Epic follows the expected data structure.
    - Ensure all required fields are populated and structured according to Jira's best practices.

    5. Feedback & Scoring
    Your output must follow this structured format:
    - If the Epics is consistent and valid, return:
    ```json
    {
        "score": "pass",
        "message": "Epics is correctly structured and consistent with the original document and
        thought instruction of each epic and within different epics."
    }
    ```
    - If the Epics is inconsistent, return:
    ```json
    {
        "score": "fail",
        "message": "Epics is inconsistent."
    }
    """,
    output_type=Feedback,
    tools=[web_search_tool],
)


# Jira Planning Process
async def perform_jira_planning(input_doc: str) -> tuple[JiraContext, list[Feedback]]:
    """
    Generates a Jira context based on the provided document.

    Args:
        input_doc (str): The input document containing project information.

    Returns:
        tuple[JiraContext, list[Feedback]]: The context containing the project overview, objectives, and epics,
        along with feedback from the consistency checks.
    """
    # Run Planning Agent to generate the thought process for each epic and associated stories and tasks
    jira_planning_result = await Runner.run(jira_planning_agent, input_doc)

    attempts = 0
    max_number_of_attempts = 5
    number_of_identified_epics = len(jira_planning_result.final_output)
    is_epics_consistent = False
    judge_feedbacks = []

    while not is_epics_consistent and attempts < max_number_of_attempts:
        """
        Iteratively runs the Jira generation and consistency check agents until the epics are consistent or the 
        maximum number of tries is reached.
        """
        # Prepare and run the Jira generation agent for each epic
        epic_generation_input_items: list[list[TResponseInputItem]] = [
            [
                {
                    "content": f"Thought Instructions: {jira_planning_result.final_output[i].jira_thought_instructions}",
                    "role": "user",
                },
                *judge_feedbacks,
            ]
            for i in range(number_of_identified_epics)
        ]
        epic_results = await asyncio.gather(
            *[
                Runner.run(jira_epic_gen_agent, input_item)
                for input_item in epic_generation_input_items
            ]
        )

        # Prepare and run the consistency check agent between the generated epics and the original document
        consistency_check_input_items = [
            {"content": f"Original Doc: {input_doc}", "role": "user"},
        ]
        for index, (jira_planning_result, epic_result) in enumerate(
            zip(jira_planning_result.final_output, epic_results), 1
        ):
            consistency_check_input_items.append(
                {
                    "content": f"Thought Instructions {index}: {jira_planning_result.jira_thought_instructions}",
                    "role": "user",
                },
            )
            consistency_check_input_items.append(
                {
                    "content": f"Jira Context {index}: {epic_result.final_output}",
                    "role": "user",
                }
            )
        consistency_check_result = await Runner.run(
            jira_consistency_check_agent,
            input=consistency_check_input_items,
            max_turns=100,
        )

        judge_feedbacks.append(consistency_check_result.final_output.feedback)
        if consistency_check_result.final_output.score == "pass":
            is_epics_consistent = True
        else:
            print(
                f"Inconsistent result: {consistency_check_result.final_output.feedback}"
            )
            is_epics_consistent = False
            attempts += 1

    if is_epics_consistent:
        print(
            f"Consistent Jira tasks and stories generated because of the following feedbacks: {judge_feedbacks}"
        )
        jira_result = JiraContext(
            epics=[epic.final_output for epic in epic_results],
        )
    else:
        print("Failed to achieve consistency after maximum tries.")
        jira_result = None

    return jira_result, judge_feedbacks
