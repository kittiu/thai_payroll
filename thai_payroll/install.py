import click

from thai_payroll.setup import after_install as setup


def after_install():
	try:
		print("Setting up Thai Payroll...")
		setup()

		click.secho("Thank you for installing Thai Payroll!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/kittiu/thai_payroll/issues/new"
		click.secho(
			"Installation for Thai Payroll app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e
