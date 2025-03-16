from dataclasses import dataclass, field
from typing import Optional, Dict, List, Set, Union
from enum import Enum, auto
from agents import trace

# Enum representing the possible states of a task
class TaskStatus(Enum):
    TODO = "TODO"           # Task not yet started
    IN_PROGRESS = "IN_PROGRESS"  # Task currently being worked on  
    DONE = "DONE"          # Task completed

class Priority(Enum):
    """Standard priority levels for work items"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    
class StoryPoints(Enum):
    """Fibonacci-style story point values"""
    XS = 1
    S = 2
    M = 3
    L = 5
    XL = 8
    XXL = 13
    UNDEFINED = 0

class WorkItemType(Enum):
    """Types of work items that can be created"""
    FEATURE = "Feature"
    BUG = "Bug"
    TECHNICAL_DEBT = "Technical Debt"
    SPIKE = "Spike"
    IMPROVEMENT = "Improvement"
    SECURITY = "Security"
    DOCUMENTATION = "Documentation"

@dataclass
class Task:
    """
    Represents a single task/work item that is part of a user story
    
    Example:
        task = Task(
            id="TASK-1",
            description="Implement login form validation",
            acceptance_criteria=["Form shows errors for invalid input", "Prevents submission when invalid"],
            technical_notes=["Use React Hook Form library"],
            assignee="john.doe",
            estimated_hours=4.0,
            dependencies={"TASK-2"},
            blocking={"TASK-3", "TASK-4"},
            work_type=WorkItemType.FEATURE,
            priority=Priority.MEDIUM
        )
    """
    id: str                           # Unique identifier for the task
    description: str                  # What needs to be done
    status: TaskStatus = TaskStatus.TODO  # Current status of the task
    work_type: WorkItemType = WorkItemType.FEATURE
    priority: Priority = Priority.MEDIUM
    acceptance_criteria: List[str] = field(default_factory=list)  # Criteria for completion
    technical_notes: List[str] = field(default_factory=list)     # Implementation details/notes
    assignee: Optional[str] = None    # Team member assigned to the task
    estimated_hours: float = 0.0      # Estimated time to complete
    dependencies: Set[str] = field(default_factory=set)  # Tasks that must be completed first
    blocking: Set[str] = field(default_factory=set)      # Tasks that cannot start until this is done

@dataclass
class UserStory:
    """
    Represents a user story that delivers business value
    
    Example:
        story = UserStory(
            id="STORY-1",
            description="As a user, I want to log in securely so that my data remains private",
            acceptance_criteria=["User can log in with valid credentials", "Invalid attempts are blocked"],
            priority=Priority.HIGH,
            story_points=StoryPoints.L,
            epic_id="EPIC-1",
            work_type=WorkItemType.FEATURE
        )
    """
    id: str                           # Unique identifier for the story
    description: str                  # User story in standard format
    work_type: WorkItemType = WorkItemType.FEATURE
    acceptance_criteria: List[str] = field(default_factory=list)  # Criteria for completion
    technical_notes: List[str] = field(default_factory=list)     # Implementation details/notes
    priority: Priority = Priority.MEDIUM
    story_points: StoryPoints = StoryPoints.UNDEFINED
    epic_id: str                      # Link to parent epic
    tasks: List[Task] = field(default_factory=list)  # Breakdown of work items
    dependencies: Set[str] = field(default_factory=set)  # Stories that must be completed first
    blocking: Set[str] = field(default_factory=set)      # Stories that cannot start until this is done

@dataclass
class Epic:
    """
    Represents a large body of work that can be broken down into multiple stories
    
    Example:
        epic = Epic(
            id="EPIC-1",
            description="User Authentication System",
            user_stories=[story1, story2]
        )
    """
    id: str                           # Unique identifier for the epic
    description: str                  # High-level description of the feature/theme
    work_type: WorkItemType = WorkItemType.FEATURE
    priority: Priority = Priority.MEDIUM
    user_stories: List[UserStory] = field(default_factory=list)  # Stories in this epic
    technical_notes: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)

@dataclass
class ProjectRequirements:
    """
    Top-level container for all project planning information
    
    Example:
        requirements = ProjectRequirements(
            project_overview="E-commerce Platform Redesign",
            objectives=["Improve conversion rate", "Reduce cart abandonment"],
            epics=[epic1, epic2],
            technical_constraints=["Must support IE11"],
            dependencies=["Payment Gateway API"],
            sprint_planning={"Sprint 1": ["STORY-1", "STORY-2"]}
        )
    """
    project_overview: str             # High-level project description
    objectives: List[str]             # Key project goals
    epics: List[Epic]                 # Major features/themes
    technical_constraints: List[str]   # Technical limitations/requirements
    dependencies: List[str]           # External system dependencies
    sprint_planning: Optional[Dict[str, List[str]]] = None  # Sprint -> Story IDs mapping
    suggestions: List[str] = field(default_factory=list)    # Improvement recommendations

# Workflow to analyze the planning requirements document and return an instance of ProjectRequirements.
async def planning_requirements_analysis(requirements_document: str) -> ProjectRequirements:
    """
    Analyze the planning requirements document and return a structured ProjectRequirements object.
    
    Args:
        requirements_document: Path or content of the requirements document
        
    Returns:
        ProjectRequirements: Structured representation of the project requirements
    """
    # Ensure the entire workflow is a single trace
    with trace("Agile requirements analysis flow"):
        # Initialize the project requirements object
        pass
