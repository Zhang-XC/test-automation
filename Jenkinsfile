node {
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

        def timedOut = false

        stage('Start Backend and Run Tests') {
            try {
                timeout(time: 1, unit: 'MINUTES') {
                    parallel {
                        stage('Start Backend') {
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
                            steps {
                                script {
                                    sh '''
                                    sleep 5
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
            } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
                cause = e.causes.get(0)
                if (cause instanceof org.jenkinsci.plugins.workflow.steps.TimeoutStepExecution.ExceededTimeout) {
                    echo "Build timed out. Proceeding to next steps."
                    timedOut = true
                } else {
                    throw e
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    sh '''
                    sleep 10
                    export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
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