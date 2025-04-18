# Check if running as administrator
#if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
#{   
#    Write-Warning "Please run this script as Administrator!"
#    break
#}

# Clear existing jobs
Get-Job | Remove-Job

# Function to start a service as a background job
function Start-VLabService {
    param (
        [string]$ServiceName,
        [int]$Port
    )
    try {
        $jobScript = {
            param($ServiceName, $Port)
            cd $using:PWD
            python -m uvicorn $ServiceName --port $Port --reload
        }
        $job = Start-Job -ScriptBlock $jobScript -ArgumentList $ServiceName, $Port
        Write-Host "Started $ServiceName on port $Port (Job ID: $($job.Id))" -ForegroundColor Green
        return $job
    }
    catch {
        Write-Error ("Failed to start {0} on port {1}: {2}" -f $ServiceName, $Port, $_.Exception.Message)
    }
}

# Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Warning "Virtual environment not found. Creating one..."
    python -m venv venv
    . .\venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}

# Array of services
$services = @(
    # Backend Services
    @{Name="backend_services.progress_tracker:app"; Port=9000},
    @{Name="backend_services.user_session:app"; Port=9001},
    @{Name="main_dashboard.backend:app"; Port=9100},
    # Project Management
    @{Name="project_management.sdlc.backend:app"; Port=8001},
    @{Name="project_management.wbs.backend:app"; Port=8002},
    @{Name="project_management.gantt.backend:app"; Port=8003},
    @{Name="project_management.resource_allocation.backend:app"; Port=8004},
    @{Name="project_management.risk_management.backend:app"; Port=8005},
    # Collaboration Tools
    @{Name="collaboration_tools.git_flow.backend:app"; Port=8006},
    @{Name="collaboration_tools.pr_merge.backend:app"; Port=8007},
    @{Name="collaboration_tools.chat_sim.backend:app"; Port=8008},
    @{Name="collaboration_tools.markdown_doc.backend:app"; Port=8009},
    @{Name="collaboration_tools.file_share.backend:app"; Port=8010},
    # Agile Methodology
    @{Name="agile_methodology.scrum_board.backend:app"; Port=8011},
    @{Name="agile_methodology.kanban.backend:app"; Port=8012},
    @{Name="agile_methodology.user_stories.backend:app"; Port=8013},
    @{Name="agile_methodology.sprint_planning.backend:app"; Port=8014},
    @{Name="agile_methodology.burndown_chart.backend:app"; Port=8015},
    # Testing Framework
    @{Name="testing_frameworks.unit_test.backend:app"; Port=8016},
    @{Name="testing_frameworks.integration_test.backend:app"; Port=8017},
    @{Name="testing_frameworks.tdd_sim.backend:app"; Port=8018},
    @{Name="testing_frameworks.test_automation.backend:app"; Port=8019},
    @{Name="testing_frameworks.ci_cd.backend:app"; Port=8020}
)

# Start all services as jobs
$jobs = @()
Write-Host "Starting backend services..." -ForegroundColor Yellow
foreach ($service in $services) {
    $jobs += Start-VLabService -ServiceName $service.Name -Port $service.Port
    Start-Sleep -Milliseconds 500
}

# Start the main dashboard
try {
    Write-Host "Starting main dashboard..." -ForegroundColor Yellow
    $dashboardJob = Start-Job -ScriptBlock {
        cd $using:PWD
        python -m streamlit run main_dashboard/main.py --server.port=8000
    }
    Write-Host "Started Main Dashboard on port 8000 (Job ID: $($dashboardJob.Id))" -ForegroundColor Green
    $jobs += $dashboardJob
}
catch {
    Write-Error ("Failed to start Main Dashboard: {0}" -f $_.Exception.Message)
}

# Monitor jobs and display output
Write-Host "`nAll services started. Monitoring output..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop all services.`n" -ForegroundColor Yellow

try {
    while ($true) {
        $jobs | ForEach-Object {
            $output = Receive-Job -Job $_
            if ($output) {
                Write-Host $output
            }
        }
        Start-Sleep -Seconds 1

        # Check for failed jobs
        $failedJobs = $jobs | Where-Object { $_.State -eq 'Failed' }
        if ($failedJobs) {
            Write-Warning "Some services have failed:"
            $failedJobs | ForEach-Object {
                Write-Error ("Job {0} failed: {1}" -f $_.Id, $_.ChildJobs[0].JobStateInfo.Reason.Message)
            }
        }
    }
}
finally {
    # Cleanup on script termination
    Write-Host "`nStopping all services..." -ForegroundColor Yellow
    $jobs | Stop-Job
    $jobs | Remove-Job
    Write-Host "All services stopped." -ForegroundColor Green
    deactivate
}
