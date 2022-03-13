$activate_script = Resolve-Path -Path ".\.venv\Scripts\Activate.ps1"
.$activate_script

$src = Resolve-Path -Path ".\src\"
cd $src

$input = Read-Host "enter alembic commit message"

python -m alembic revision --autogenerate -m $input

python -m alembic upgrade head

cd ..