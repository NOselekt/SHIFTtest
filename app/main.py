from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pathlib import Path

from routers import EmployeeSalaryRouter

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)

@app.get("/")
async def main() -> RedirectResponse:
	'''
    Responsible for the main page.
    :return: redirects to the page with employee's salary info.
    '''
	return RedirectResponse("/employee_salary")


app.include_router(EmployeeSalaryRouter.router)