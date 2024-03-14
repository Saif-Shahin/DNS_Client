import CommandLineInput
import SendQuery

def main():
    # Parse command line arguments
    args = CommandLineInput.get_args()

    # Send the query using the parsed arguments
    SendQuery.sendQuery(args)

if __name__ == "__main__":
    main()
