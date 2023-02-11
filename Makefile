run:
	cls
	@echo Run project with scriptfile...
	@python .\main.py


test:
	cls
	@echo "Run PyTest ..."
	@pytest
	@echo "PyTest finished!"

clean:
	cls
	@echo Clean up project files...
	@if exist ".\build" rd /q /s build
	@if exist ".\dist" rd /q /s dist
	@if exist ".pytest_cache" rd /q /s .pytest_cache 
	@if exist ".\src\__pycache__" rd /q /s .\src\__pycache__
	@if exist ".\tests\__pycache__" rd /q /s .\tests\__pycache__
	@echo Clean up finished!

build:
	cls
	@echo Start building process...
	@pyinstaller .\config\main.spec
	@explorer .\dist\BreakOut
	@echo Buil is finished