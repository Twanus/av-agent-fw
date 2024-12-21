from agent import Agent

if __name__ == "__main__":
    agent = Agent()

    # Define the command you want to run on the remote hosts
    command = "echo 'Hello, World!'"

    # Run the command on all hosts
    agent.run_ssh_command(command)
