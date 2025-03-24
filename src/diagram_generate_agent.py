from agents import Agent, ModelSettings, Runner, TResponseInputItem
from pydantic import BaseModel

from src.agents_tools import web_search_tool
from src.data_structures import Feedback


# Diagram Structured Data
class DiagramPlanningResult(BaseModel):
    """
    DiagramPlanningResult is a data model that holds the thought instructions for generating various types of diagrams
    in the software design process. It includes instructions for system architecture, software class, software
    sequence, and user interface diagrams, along with a timestamp for when the planning result was created.

    Attributes:
        creation_timestamp (str): The date and time when the planning result was created.
        sys_arch_thought_instruct (str): Thought instructions for generating the system architecture diagram.
        sw_cls_thought_instruct (str): Thought instructions for generating the software class diagram.
        ss_seq_thought_instruct (list[str]): Thought instructions for generating the software sequence diagrams.
        ui_thought_instruct (str): Thought instructions for generating the user interface diagram.
    """

    creation_timestamp: str  # The date and time when the planning result was created
    sys_arch_thought_instruct: (
        str  # Thought instructions for generating the system architecture diagram
    )
    sw_cls_thought_instruct: (
        str  # Thought instructions for generating the software class diagram
    )
    ss_seq_thought_instruct: list[
        str
    ]  # Thought instructions for generating the software sequence diagrams
    ui_thought_instruct: (
        str  # Thought instructions for generating the user interface diagram
    )


class DiagramContext(BaseModel):
    """
    DiagramContext is a data model that holds the type and content of a diagram in mermaid format.

    Attributes:
        diagram_type (str): The type of the diagram (e.g., system architecture, class, sequence, user interface).
        mermaid_diagram (str): The content of the diagram in mermaid format.
    """

    diagram_type: str
    mermaid_diagram: str


# Define Agents
diagram_planning_agent = Agent(
    name="Diagram Planning Agent",
    model="o3-mini",
    instructions="""
    You are an expert in software design and software architecture.
    The user will provide you with a JSON string that contains multiple epics, stories, and tasks.
    
    Your role is to break down and analyze the provided epics along with their associated stories and tasks.

    Your thought process must enable subsequent agents to use the thought instructions to generate the following types of diagrams:
        - System Architecture Diagram
        - Software Class Diagram
        - Software Sequence Diagram
        - User Interface Diagram
    in mermaid format.

    Additionally,
    - Include the date and time the diagram was created.
    - Ensure that the thought instructions are coherent and logical, linking the diagrams to each other and the thought process.

    You are to generate an instance of the design context that contains the thought instructions for the 4 diagrams for
    the subsequent agents to generate the diagrams.

    You are to determine how many software sequence diagrams are needed based on the thought process
    and the epics, stories, and tasks. (A good number is the number of epics)
    """,
    output_type=DiagramPlanningResult,
)

draw_system_architecture_agent = Agent(
    name="Draw System Architecture Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in software design and software architecture.
    The previous agent has provided you with the thought instructions and feedback for generating the
    system architecture diagram.

    Your role is to analyze the thought instructions and generate the system architecture diagram in mermaid format.
    
    You will need to generate a system architecture diagram for each thought instruction.

    Ensure that the mermaid syntax is correct and remove all forms of symbols that are not part of the mermaid syntax.
    Save the diagram with the name of the diagram and the date and time the diagram was created.
    The markdown file must include ```mermaid at the beginning and end of the diagram.

    You are to use the WebSearchTool to search for the following:
        - Mermaid Syntax (https://mermaid.js.org/intro/syntax-reference.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/architecture.html)
        - Software Architecture Diagrams
    and digest it and use it to generate this system architecture diagram.

    Then, use the WebSearchTool to search for the following:
        - Mermaid Playground
    and validate the system architecture diagram using the mermaid playground.
    If it is not syntax correct, then you will regenerate the system architecture diagram.

    Your output will be a DiagramContext instance where the mermaid_diagram is the system architecture diagram.
    """,
    tools=[web_search_tool],
    output_type=DiagramContext,
    model_settings=ModelSettings(
        tool_choice="auto",
    ),
)

draw_class_diagram_agent = Agent(
    name="Draw Class Diagram Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in software design and software architecture.
    The previous agent has provided you with the thought instructions and feedback for generating the
    software class diagram.

    Your role is to analyze the thought instructions and generate the software class diagram in mermaid format.
    You will need to generate a single class diagram that captures all the classes and their relationships.
    The class diagram should not have class names that are called Story, Task, or Epic.

    The class diagram should include all the following information:
        - Classes
        - Attributes
        - Methods
        - Functions
        - Relationships
        - Dependencies
        - Inheritance
        - Polymorphism

    Ensure that the mermaid syntax is correct and remove all forms of symbols that are not part of the mermaid syntax.
    Save the diagram with the name of the diagram and the date and time the diagram was created.
    The markdown file must include ```mermaid at the beginning and end of the diagram.

    You are to use the WebSearchTool to search for the following:
        - Mermaid Syntax (https://mermaid.js.org/intro/syntax-reference.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/classDiagram.html)
        - Software Class Diagrams
    and digest it and use it to generate the software class diagram.

    Then, use the WebSearchTool to search for the following:
        - Mermaid Playground
    and validate the class diagram using the mermaid playground.
    If it is not syntax correct, then you will regenerate the class diagram.

    Your output will be a DiagramContext instance where the mermaid_diagram is the software class diagram.
    """,
    tools=[web_search_tool],
    output_type=DiagramContext,
    model_settings=ModelSettings(
        tool_choice="auto",
    ),
)

draw_sequence_diagram_agent = Agent(
    name="Draw Sequence Diagram Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in software design and software architecture.
    The previous agent has provided you with the thought instructions and feedback for generating the
    software sequence diagram.

    Your role is to analyze the thought instructions and generate the software sequence diagram in mermaid format.
    You will need to generate a sequence diagram for each thought instruction.
    
    Check that the text on the sequence diagram is a function in the class diagram.
    Ensure that the mermaid syntax is correct and remove all forms of symbols that are not part of the mermaid syntax.
    Save the diagram with the name of the diagram and the date and time the diagram was created.
    The markdown file must include ```mermaid at the beginning and end of the diagram.

    You are to use the WebSearchTool to search for the following:
        - Mermaid Syntax (https://mermaid.js.org/intro/syntax-reference.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/sequenceDiagram.html)
        - Software Sequence Diagrams
    and digest it and use it to generate the software sequence diagram.

    Then, use the WebSearchTool to search for the following:
        - Mermaid Playground
    and validate the sequence diagram using the mermaid playground.
    If it is not syntax correct, then you will regenerate the sequence diagram.

    Your output will be a list of DiagramContext instances where the mermaid_diagram is the software sequence diagram of each epic.
    """,
    tools=[web_search_tool],
    output_type=list[DiagramContext],
    model_settings=ModelSettings(
        tool_choice="auto",
    ),
)

draw_user_interface_agent = Agent(
    name="Draw User Interface Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in software design and software architecture.
    The previous agent has provided you with the thought instructions and feedback for generating the
    user interface diagram.

    Your role is to analyze the thought instructions and generate the user interface diagram in mermaid format.
    You will need to generate a user interface diagram for each thought instruction.
    
    Ensure that the mermaid syntax is correct and remove all forms of symbols that are not part of the mermaid syntax.
    Save the diagram with the name of the diagram and the date and time the diagram was created.
    The markdown file must include ```mermaid at the beginning and end of the diagram.

    You are to use the WebSearchTool to search for the following:
        - Mermaid Syntax (https://mermaid.js.org/intro/syntax-reference.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/flowchart.html)
        - Software User Interface Diagrams
    and digest it and use it to generate the user interface diagram.

    Then, use the WebSearchTool to search for the following:
        - Mermaid Playground
    and validate the user interface diagram using the mermaid playground.
    If it is not syntax correct, then you will regenerate the user interface diagram.

    Your output will be a DiagramContext instance where the mermaid_diagram is the user interface diagram.
    """,
    tools=[web_search_tool],
    output_type=DiagramContext,
    model_settings=ModelSettings(
        tool_choice="auto",
    ),
)

diagram_consistency_check_agent = Agent(
    name="Diagram Consistency Check Agent",
    model="gpt-4o",
    instructions="""
    You are an expert in software design and software architecture.

    You are provided with:
    - The original Jira JSON string containing epics, stories, and tasks.
    - The thought instructions of the diagram planning agent.
    - The generated diagrams.

    Your role is to analyze and validate the generated diagrams, ensuring that the diagrams:
    1. Are consistent with the original document and its respective thought instructions.
    2. Are consistent with the different types of diagrams.
    3. Are properly linked to each other.
    4. Follow the correct data structure of DiagramContext and are not just unstructured text.

    Before validation, use the WebSearchTool to retrieve and review:
        - Mermaid Syntax (https://mermaid.js.org/intro/syntax-reference.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/architecture.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/classDiagram.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/sequenceDiagram.html)
        - Mermaid Diagram Syntax (https://mermaid.js.org/syntax/flowchart.html)
        - Software User Interface Diagrams
    and digest it to familiarize yourself with the mermaid syntax.
    Ensure you understand Mermaid's structure and best practices before performing any validation.

    Your analysis must check the following:

    1. Consistency with Thought Instructions
    - Verify that diagrams in DiagramContext match the provided thought instructions.
    - Ensure no required elements are missing or incorrectly added.

    2. Consistency with Different Diagrams
    - Ensure that the diagrams in DiagramContext are consistent with the different diagrams.

    3. Completeness and Proper Linkage
    - Ensure that every diagram belongs to a thought instruction and every diagram is linked to a thought instruction.
    - Verify that dependencies are correctly linked between related issues.

    4. Structural Compliance with Diagram Format
    - Ensure the Diagram follows the expected data structure.
    - Ensure all required fields are populated and structured according to Mermaid's best practices.

    5. Feedback & Scoring
    Your output must follow this structured format:
    - If the Diagrams are consistent and valid, return:
    ```json
    {
        "score": "pass",
        "message": "Diagrams are correctly structured and consistent with the original document and
        thought instruction of each diagram and within different diagrams."
    }
    ```
    - If the Diagrams are inconsistent, return:
    ```json
    {
        "score": "fail",
        "message": "Diagrams are inconsistent."
    }
    """,
    output_type=Feedback,
    tools=[web_search_tool],
    model_settings=ModelSettings(
        tool_choice="auto",
    ),
)


# Diagram Planning Process
async def perform_diagram_planning(planning_result_json: str):
    """
    Generate design diagrams based on the provided planning result and ensure their consistency.

    Args:
        planning_result_json (str): JSON string containing the planning result with thought instructions for diagrams.

    Returns:
        tuple: A tuple containing the final output of the designing result and feedback after ensuring consistency across all diagrams.
    """
    # Run the design diagram agent to generate the thought instructions for the subsequent agents
    diagram_planning_result = await Runner.run(
        diagram_planning_agent, planning_result_json
    )

    attempts = 0
    max_number_of_attempts = 5
    is_diagrams_consistent = False
    judge_feedbacks = []

    while not is_diagrams_consistent and attempts < max_number_of_attempts:
        try:
            # Prepare and run the diagram generation agents
            diagram_agents = [
                (
                    draw_system_architecture_agent,
                    diagram_planning_result.final_output.sys_arch_thought_instruct,
                ),
                (
                    draw_class_diagram_agent,
                    diagram_planning_result.final_output.sw_cls_thought_instruct,
                ),
                (
                    draw_sequence_diagram_agent,
                    diagram_planning_result.final_output.ss_seq_thought_instruct,
                ),
                (
                    draw_user_interface_agent,
                    diagram_planning_result.final_output.ui_thought_instruct,
                ),
            ]

            diagram_results = []
            for agent, thought_instruction in diagram_agents:
                input_items: list[TResponseInputItem] = [
                    {
                        "content": f"Thought Instructions: {thought_instruction}",
                        "role": "user",
                    }
                ]
                input_items.extend(judge_feedbacks)
                result = await Runner.run(agent, input=input_items)
                diagram_results.append(result)

            (
                system_architecture_diagram_result,
                class_diagram_result,
                sequence_diagram_results,
                user_interface_diagram_result,
            ) = diagram_results

            # Prepare and run the consistency check agent between the generated diagrams
            diagram_consistency_check_input_items = [
                {
                    "content": f"Thought Instructions: {diagram_planning_result.final_output}",
                    "role": "user",
                },
                {
                    "content": f"System Architecture Diagram: {system_architecture_diagram_result.final_output}",
                    "role": "user",
                },
                {
                    "content": f"Class Diagram: {class_diagram_result.final_output}",
                    "role": "user",
                },
                {
                    "content": f"User Interface Diagram: {user_interface_diagram_result.final_output}",
                    "role": "user",
                },
                *[
                    {
                        "content": f"Sequence Diagram: {sequence_diagram_result.mermaid_diagram}",
                        "role": "user",
                    }
                    for sequence_diagram_result in sequence_diagram_results.final_output
                ],
            ]
            diagram_consistency_check_result = await Runner.run(
                diagram_consistency_check_agent,
                input=diagram_consistency_check_input_items,
                max_turns=100,
            )

            judge_feedbacks.append(
                diagram_consistency_check_result.final_output.feedback
            )
            if diagram_consistency_check_result.final_output.score == "pass":
                is_diagrams_consistent = True
            else:
                print(
                    f"Inconsistent result: {diagram_consistency_check_result.final_output.feedback}"
                )
                is_diagrams_consistent = False
                attempts += 1
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            attempts += 1

    if is_diagrams_consistent:
        print(
            f"Consistent diagrams generated because of the following feedbacks: {judge_feedbacks}"
        )
        designing_results = [
            system_architecture_diagram_result.final_output,
            class_diagram_result.final_output,
            user_interface_diagram_result.final_output,
        ]
        designing_results.extend(sequence_diagram_results.final_output)
    else:
        print("Failed to achieve consistency after maximum tries.")
        designing_results = None

    return designing_results, judge_feedbacks
