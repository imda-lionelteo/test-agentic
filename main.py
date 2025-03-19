
import asyncio
from dataclasses import field
from enum import Enum
import os
from typing import Optional, Union
from pydantic import BaseModel

from docx import Document
from agents import Runner, trace, Agent, function_tool

# Enum representing the possible states of a task
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
    Enum defining standard priority levels for tasks.

    Attributes:
        CRITICAL (str): Highest priority level.
        HIGH (str): High priority level.
        MEDIUM (str): Medium priority level.
        LOW (str): Low priority level.
    """
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class StoryPoints(Enum):
    """
    Enum defining Fibonacci-style story point values for estimating task complexity.

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
    Represents a single task or work item that is part of a user story.

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

    Example:
        task = Task(
            task_id="TASK-1",
            name="Implement login form validation",
            description="Implement validation for the login form.",
            status=TaskStatus.IN_PROGRESS,
            priority=Priority.HIGH,
            acceptance_criteria=[
                "Form shows errors for invalid input",
                "Prevents submission when invalid input is detected"
            ],
            technical_notes=["Use React Hook Form library"],
            assignee="john.doe",
            estimated_hours=4.0,
            linked_issues=["TASK-2"]
        )
    """
    task_id: str  # Unique identifier for the task
    name: str  # Name of the task
    description: str  # Detailed description of what needs to be done
    status: TaskStatus = TaskStatus.TODO  # Current status of the task, default is TaskStatus.TODO
    priority: Priority = Priority.MEDIUM  # Priority level of the task, default is Priority.MEDIUM
    acceptance_criteria: list[str] = field(default_factory=list)  # List of criteria for task completion
    technical_notes: list[str] = field(default_factory=list)  # List of technical notes or implementation details
    assignee: Optional[str] = None  # Team member assigned to the task, default is None
    estimated_hours: Optional[float] = None  # Estimated time required to complete the task, default is None
    linked_issues: list[str] = field(default_factory=list)  # List of tasks that are linked to this task

class Story(BaseModel):
    """
    Represents a user story that delivers business value.

    Attributes:
        story_id (str): Unique identifier for the story.
        name (str): Name of the story.
        description (str): Detailed description of the user story.
        status (TaskStatus): Current status of the story, default is TaskStatus.TODO.
        priority (Priority): Priority level of the story, default is Priority.MEDIUM.
        acceptance_criteria (list[str]): List of criteria that must be met for the story to be considered complete.
        technical_notes (list[str]): List of technical notes or implementation details.
        assignee (Optional[str]): Team member assigned to the story, default is None.
        estimated_hours (Optional[float]): Estimated time required to complete the story, default is None.
        linked_issues (list[str]): List of tasks that are linked to this story.

    Example:
        story = Story(
            story_id="STORY-1",
            name="Secure Login",
            description="As a user, I want to log in securely so that my data remains private.",
            status=TaskStatus.TODO,
            priority=Priority.HIGH,
            acceptance_criteria=[
                "User can log in with valid credentials",
                "Invalid login attempts are blocked"
            ],
            technical_notes=["Ensure encryption of passwords"],
            assignee="jane.doe",
            estimated_hours=5.0,
            linked_issues=["TASK-3"]
        )
    """
    story_id: str  # Unique identifier for the story
    name: str  # Name of the story
    description: str  # Detailed description of the user story
    status: TaskStatus = TaskStatus.TODO  # Current status of the story, default is TaskStatus.TODO
    priority: Priority = Priority.MEDIUM  # Priority level of the story, default is Priority.MEDIUM
    acceptance_criteria: list[str] = field(default_factory=list)  # List of criteria for story completion
    technical_notes: list[str] = field(default_factory=list)  # List of technical notes or implementation details
    assignee: Optional[str] = None  # Team member assigned to the story, default is None
    estimated_hours: Optional[float] = None  # Estimated time required to complete the story, default is None
    linked_issues: list[str] = field(default_factory=list)  # List of tasks that are linked to this story

class Epic(BaseModel):
    """
    Represents a large body of work that can be broken down into multiple stories.

    Attributes:
        id (str): Unique identifier for the epic.
        name (str): Name of the epic.
        description (str): High-level description of the feature/theme.
        priority (Priority): Priority level, default is Priority.MEDIUM.
        child_issues (list[Union[Task, Story]]): List of child tasks or stories associated with the epic.

    Example:
        epic = Epic(
            id="EPIC-1",
            name="User Authentication System",
            description="User Authentication System",
            priority=Priority.HIGH,
            child_issues=[task1, story1]
        )
    """
    id: str  # Unique identifier for the epic
    name: str  # Name of the epic
    description: str  # High-level description of the feature/theme
    priority: Priority = Priority.MEDIUM  # Priority level, default is Priority.MEDIUM
    child_issues: list[Union[Task, Story]] = field(default_factory=list)  # List of child tasks or stories associated with the epic

class JiraContext(BaseModel):
    """
    Top-level container for all project planning information.

    Attributes:
        project_overview (str): High-level project description.
        objectives (list[str]): Key project goals.
        epics (list[Epic]): Major features/themes.
        dependencies (list[str]): External system dependencies.

    Example:
        requirements = JiraContext(
            project_overview="E-commerce Platform Redesign",
            objectives=["Improve conversion rate", "Reduce cart abandonment"],
            epics=[epic1, epic2],
            dependencies=["Payment Gateway API"]
        )
    """
    project_overview: str  # High-level project description
    objectives: list[str]  # Key project goals
    epics: list[Epic]  # Major features/themes
    dependencies: list[str]  # External system dependencies

@function_tool
def write_json_file(file_name: str, json_data: str) -> str:
    """
    Writes the provided JSON data to a file in the 'generated/planning' directory.

    Args:
        file_name (str): The name of the file to write the JSON data to.
        json_data (str): The JSON data to be written to the file.

    Returns:
        str: The path to the file where the JSON data was written.
    """
    directory = "generated/planning"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    print(f"Writing JSON data to file: {file_path}")
    with open(file_path, "w") as f:
        f.write(json_data)
    return file_path

@function_tool
def write_mermaid_file(file_name: str, mermaid_text: str) -> str:
    """
    Writes the provided Mermaid text to a file in the 'generated/design' directory.

    Args:
        file_name (str): The name of the file to write the Mermaid text to.
        mermaid_text (str): The Mermaid text to be written to the file.

    Returns:
        str: The path to the file where the Mermaid text was written.
    """
    directory = "generated/design"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    print(f"Writing mermaid text to file: {file_path}")
    with open(file_path, "w") as f:
        f.write(mermaid_text)
    return file_path

planning_agent = Agent(
    name="Planning Workflow Agent",
    instructions="""
    As an expert product owner, After reviewing all the generated options, the best set of instructions is the one that clearly lays out concrete steps with explicit details about the JSON structure, provides an example, and includes all required information (file formatting, naming conventions, and the call to write_json_file).
    Review the planning requirements document and convert it into structured Jira-compatible JSON objects, including epics, stories, and tasks.
    Ensure each object has the following fields and filled with the relevant values:
    - id  
    - name  
    - description  
    - status  
    - priority  
    - acceptanceCriteria  
    - technicalNotes  
    - assignee  
    - estimatedHours  
    - linkedIssues

    Populate each field with relevant values from the document.
    Export the data as a JSON file with 4-space indentation, using clear, descriptive filenames ending with “.json” (for example, epics.json, stories.json, tasks.json).
    
    Finally, use the write_json_file tool to save the JSON file.
    Example JSON Structure:
    {
        "id": "EPIC-001",
        "name": "Epic Example",
        "description": "Detailed description of the epic.",
        "status": "To Do",
        "priority": "High",
        "acceptanceCriteria": "Acceptance criteria for this epic.",
        "technicalNotes": "Technical implementation details.",
        "assignee": "John Doe",
        "estimatedHours": 40,
        "linkedIssues": ["STORY-002", "TASK-003"]
    }
    """,
    output_type=JiraContext,
    model="o3-mini",
    tools=[write_json_file]
)

designing_agent = Agent(
    name="Design Workflow Agent",
    instructions="""
    As an expert in software design, Analyze the provided epics along with their associated stories and tasks to create detailed mermaid diagrams.
    
    Your deliverables must include three types of diagrams:
    1. Class Diagrams:
    - Include all classes, interfaces, and relationships.
    - Capture inheritance, associations, and dependencies.
    - Ensure the mermaid syntax is correct and remove all forms of symbols like arrows, etc and follow the mermaid format.
    - Save as "class_diagram.md" and it should be a markdown file with ```mermaid at the beginning and ``` at the end.

    2. Architecture Diagrams:
    - Include all components, services, and their interactions.
    - Illustrate overall system architecture and component integration.
    - Ensure the mermaid syntax is correct and remove all forms of symbols like arrows, etc and follow the mermaid format.
    - Save as "architecture_diagram.md" and it should be a markdown file with ```mermaid at the beginning and ``` at the end.

    3. Sequence Diagrams:
    - Include all sequences, interactions, and message flows.
    - The classes should be the same as the class diagrams.
    - Show the order of operations and method calls.
    - Break down the sequence diagrams into multiple diagrams for each epic.
    - Ensure the mermaid syntax is correct and remove all forms of symbols like arrows, etc and follow the mermaid format.
    - Save as "sequence_diagram_{epic_id}.md" and it should be a markdown file with ```mermaid at the beginning and ``` at the end.

    4. System Diagrams:
    - Include all components, services, and their interactions.
    - Illustrate overall system architecture and component integration.
    - Ensure the mermaid syntax is correct and remove all forms of symbols like arrows, etc and follow the mermaid format.
    - Save as "system_diagram.md" and it should be a markdown file with ```mermaid at the beginning and ``` at the end.

    It is important that this 4 diagrams must be generated.
    """,
    model="o3-mini",
    tools=[
        write_mermaid_file,
    ]
)

async def main():
    # input_prompt = input("Provide the link to the agile requirements document: ")
    input_prompt = "sample.docx"

    # Read the file
    if input_prompt.endswith(".docx"):
        doc = Document(input_prompt)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        print("File is not a docx file")
        exit(0)

    with trace("Software development workflow"):
        # Run the planning agent
        planning_result = await Runner.run(planning_agent, text)
        
        # Use a design agent to generate a design
        designing_result = await Runner.run(designing_agent, input=f"{planning_result.final_output}", max_turns=50)

        # TODO: Use a development agent to generate code

        # TODO: Use a testing agent to generate tests

        # TODO: Use a deployment agent to deploy the code

        # TODO: Use a monitoring agent to monitor the application

        # TODO: Use a feedback agent to get feedback on the application 

if __name__ == "__main__":
    asyncio.run(main())
