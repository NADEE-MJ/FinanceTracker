$activate_script = Resolve-Path -Path ".\.venv\Scripts\Activate.ps1"
.$activate_script

$src = Resolve-Path -Path ".\src\"
cd $src

Start-Job -Name Server -ScriptBlock {uvicorn api.main:app --reload}

while($true) {
    $input = Read-Host "Stop Server (y)"

    if($input -eq "y") {
        Stop-Job -Name Server
        break
    }
}

cd ..
# deactivate