def unsafe(app, args, out, virtual_input):
    """
    Decorator for unsafe commands.

    This decorator is designed for commands that may raise exceptions during execution.
    It wraps the execution of the specified `app` function, catches any exceptions,
    clears the output buffer, prints the error message, and returns the cleared output.

    Parameters:
    - app (function): The function representing the unsafe command.
    - args (list): The arguments to be passed to the `app` function.
    - out (deque): The output deque to capture the command's output.
    - virtual_input (deque): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the unsafe commands,
                   returns empty deque if exceptions raised.
    """
    try:
        return app(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
