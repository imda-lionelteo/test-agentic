import asyncio

from agents import trace
from docx import Document

from src.diagram_generate_agent import perform_diagram_planning
from src.jira_planning_agent import perform_jira_planning
from src.utils import write_to_file


async def main():
    # For testing purposes, the input document is hardcoded.
    # Uncomment the following line to prompt the user for input:
    # input_prompt = input("Provide the link to the agile requirements document: ")
    input_prompt = "sample.docx"

    # Read the file and extract text if it is a .docx file
    if input_prompt.endswith(".docx"):
        doc = Document(input_prompt)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        print("The provided file is not a .docx file.")
        exit(0)

    with trace("Software development workflow"):
        # Run the Jira planning agent to generate the planning result
        jira_planning_result, judge_feedbacks = await perform_jira_planning(text)
        if jira_planning_result:
            write_to_file(
                jira_planning_result.model_dump_json(indent=4),
                "jira_planning",
                "jira_planning.json",
            )
        else:
            feedback_messages_str = "\n".join(
                feedback.feedback for feedback in judge_feedbacks
            )
            print(
                f"No Jira planning result was generated because {feedback_messages_str}"
            )
            exit(1)

        # Use a diagram generation agent to generate a design
        diagram_planning_results, judge_feedbacks = await perform_diagram_planning(
            jira_planning_result.model_dump_json(indent=4)
        )
        if diagram_planning_results:
            for diagram_planning_result in diagram_planning_results:
                write_to_file(
                    diagram_planning_result.mermaid_diagram,
                    "diagrams",
                    f"{diagram_planning_result.diagram_type}.md",
                )
        else:
            feedback_messages_str = "\n".join(
                feedback.feedback for feedback in judge_feedbacks
            )
            print(
                f"No diagram planning results were generated because {feedback_messages_str}"
            )
            exit(1)

        # TODO: Use a development agent to generate code
        # code_generation_result = await Runner.run(code_generation_agent, input=f"{designing_result.final_output}", max_turns=50)

        # TODO: Use a testing agent to generate tests

        # TODO: Use a deployment agent to deploy the code

        # TODO: Use a monitoring agent to monitor the application

        # TODO: Use a feedback agent to get feedback on the application


if __name__ == "__main__":
    asyncio.run(main())
