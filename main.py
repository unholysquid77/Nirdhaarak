import ast
from core.orchestrator import Orchestrator


def extract_list(text):
    """
    Extract a Python-style list from the user input.
    Example:
    predict grade [1,2,3]
    """

    try:

        start = text.index("[")
        end = text.index("]") + 1

        list_str = text[start:end]

        data = ast.literal_eval(list_str)

        if isinstance(data, list):
            return data

    except Exception:
        return None

    return None


def main():

    bot = Orchestrator()

    print("\nStudent Academic AI Assistant")
    print("--------------------------------")
    print("Commands:")
    print("predict grade [list_of_15_features]")
    print("exit\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        if "predict grade" in user_input.lower():

            student_data = extract_list(user_input)

            response = bot.run_grade_prediction(student_data)

        else:

            response = bot.run(user_input)

        print("\nBot:", response)
        print()


if __name__ == "__main__":
    main()