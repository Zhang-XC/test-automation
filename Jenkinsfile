pipeline {
    agent any

    environment {
        PYTHONPATH = '..'
    }

    stages {
        stage('Clean Previous Report') {
            steps {
                powershell '''
                if (Test-Path -Path test_framework\\report\\temp) {
                    Remove-Item -Recurse -Force test_framework\\report\\temp
                }
                '''
            }
        }

        stage('Start Backend') {
            steps {
                powershell '''
                Start-Process -NoNewWindow -FilePath uv -ArgumentList 'run', 'backend/app.py'
                '''
                sleep(time: 5, unit: 'SECONDS')
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                uv run test_framework/main.py
                '''
            }
        }

        stage('Publish Allure Report') {
            steps {
                publishHTML(target: [
                    reportDir: 'test_framework/report/temp',
                    reportFiles: 'index.html',
                    reportName: 'Allure Report'
                ])
            }
        }
    }

    post {
        always {
            powershell '''
            Get-Process uv -ErrorAction SilentlyContinue | Stop-Process -Force
            '''
        }
    }
}