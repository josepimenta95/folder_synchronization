class InsufficientCommandLineArguments(Exception):
    def __init__(self, number_of_arguments_given):
        self.number_of_arguments_given = number_of_arguments_given
        super().__init__(
            f"Insufficient Command Line Arguments: {self.number_of_arguments_given} arguments given, when 4 were expected"
        )


class InvalidCommandLineArgument(Exception):
    def __init__(self, arguments_invalid_dict: dict):
        self.arguments_invalid_dict = arguments_invalid_dict
        message = "CommandLineArgumentsInvalid:\n"
        for argument in arguments_invalid_dict:
            message += f"{argument}: {arguments_invalid_dict[argument]}\n"
        super().__init__(message)
