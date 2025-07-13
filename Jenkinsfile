pipeline {
    agent any

    stages {
        stage('Clean Previous Report') {
            steps {
                script {
                    sh '''
                    if [ -d test_framework/report/temp ]; then
                        rm -rf test_framework/report/temp
                    fi
                    '''
                }
            }
        }

        stage('Start Backend and Run Tests') {
            parallel {
                stage('Start Backend') {
                    options {
                        timeout(time: 2, unit: 'MINUTES')
                    }
                    steps {
                        script {
                            sh '''
                            cd backend_service
                            export PYTHONPATH=".."
                            export PATH=$PATH:/home/ubuntu/.local/bin
                            uv run app.py
                            '''
                        }
                    }
                }

                stage('Run Tests') {
                    options {
                        timeout(time: 2, unit: 'MINUTES')
                    }
                    steps {
                        script {
                            sh '''
                            sleep 10
                            cd test_framework
                            export PYTHONPATH=".."
                            export PATH=$PATH:/home/ubuntu/.local/bin
                            uv run main.py
                            '''
                        }
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    sh '''
                    sleep 20
                    allure generate test_framework/report/temp -o test_framework/report/html
                    '''
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
                sh 'pkill -u jenkins -x uv || true'
            }
        }
    }
}