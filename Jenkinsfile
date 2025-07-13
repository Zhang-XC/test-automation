pipeline {
    agent any

    stages {
        stage('Clean Previous Report') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        if [ -d test_framework/report/temp ]; then
                            rm -rf test_framework/report/temp
                        fi
                        '''
                    } else {
                        powershell '''
                        if (Test-Path -Path test_framework\\report\\temp) {
                            Remove-Item -Recurse -Force test_framework\\report\\temp
                        }
                        '''
                    }
                }
            }
        }

        stage('Start Backend') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        cd backend_service
                        export PYTHONPATH=".."
                        export PATH=$PATH:/home/ubuntu/.local/bin
                        uv run app.py
                        '''
                    } else {
                        powershell '''
                        cd backend_service
                        $env:PYTHONPATH = ".."
                        uv run app.py
                        '''
                    }
                }
                sleep(time: 5, unit: 'SECONDS')
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        cd test_framework
                        export PYTHONPATH=".."
                        export PATH=$PATH:/home/ubuntu/.local/bin
                        uv run main.py
                        '''
                    } else {
                        powershell '''
                        cd test_framework
                        $env:PYTHONPATH = ".."
                        uv run main.py
                        '''
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        allure generate test_framework/report/temp -o test_framework/report/html
                        '''
                    } else {
                        powershell '''
                        allure generate test_framework\\report\\temp -o test_framework\\report\\html
                        '''
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                publishHTML(target: [
                    reportDir: 'test_framework/report/html',
                    reportFiles: 'index.html',
                    reportName: 'Allure Report'
                ])
            }
        }
    }

    post {
        always {
            script {
                if (isUnix()) {
                    sh 'pkill -x uv || true'
                } else {
                    powershell '''
                    Get-Process uv -ErrorAction SilentlyContinue | Stop-Process -Force
                    '''
                }
            }
        }
    }
}