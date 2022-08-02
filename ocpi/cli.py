import random
import typer
import questionary

app = typer.Typer()


@app.command()
def start():
    program_continue = typer.confirm("You have just started OCPI app, do you want to continue")
    if not program_continue:
        raise typer.Abort()

    # Charge point information
    cp_serial_number = typer.prompt("Enter charge point serial number")
    central_system_url = typer.prompt("Enter central system URL")

    # Connection mocking
    string = "You are connecting to %s charge point via %s"
    typer.echo(string % (cp_serial_number, central_system_url))
    # TODO: Random function is just to check functionality of typer command, later we will implement real connection
    connection = random.choice([True, False])  # nosec
    if not connection:
        typer.echo('Connection was unsuccessful. In order to try again you need to call start command.')
        raise typer.Abort()

    answer = questionary.select(
        "What action do you want to perform: ",
        choices=[
            'Quit',
            'Send an OCPP message'
        ]
    ).ask()

    if answer == 'Quit':
        raise typer.Abort()

    ocpp_message = typer.prompt('Enter your OCPP message')
    typer.echo(ocpp_message)


if __name__ == '__main__':
    app()
