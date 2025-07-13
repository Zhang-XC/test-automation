node {
    stage('Clean Previous Report') {
        sh '''
        if [ -d ./report/temp ]; then
            rm -rf ./report/temp/*
        fi
        if [ -d ./report/html ]; then
            rm -rf ./report/html/*
        fi
        if [ -d ./gh-pages ]; then
            rm -rf gh-pages
        fi
        '''
    }

    def timedOut = false

    stage('Start Backend and Run Tests') {
        try {
            timeout(time: 1, unit: 'MINUTES') {
                parallel(
                    'Start Backend': {
                        sh '''
                        cd backend_service
                        export PYTHONPATH=".."
                        export PATH=$PATH:/home/ubuntu/.local/bin
                        uv run app.py
                        '''
                    },
                    'Run Tests': {
                        sh '''
                        sleep 5
                        cd test_framework
                        export PYTHONPATH=".."
                        export PATH=$PATH:/home/ubuntu/.local/bin
                        uv run main.py
                        '''
                    }
                )
            }
        } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
            def cause = e.causes.get(0)
            if (cause instanceof org.jenkinsci.plugins.workflow.steps.TimeoutStepExecution.ExceededTimeout) {
                echo "Build timed out. Proceeding to next steps."
                timedOut = true
            } else {
                throw e
            }
        }
    }

    stage('Generate Allure Report') {
        sh '''
        sleep 10
        export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
        mkdir ./report/html
        allure generate ./report/temp -o ./report/html
        '''
    }

    stage('Publish Allure Report') {
        publishHTML(target: [
            reportDir: './report/html',
            reportFiles: 'index.html',
            reportName: 'Allure Report',
            keepAll: true,
            alwaysLinkToLastBuild: true,
            allowMissing: false
        ])
    }

    stage('Deploy Allure Report') {
        withCredentials([string(credentialsId: 'github-token', variable: 'GIT_TOKEN')]) {
            sh '''
                git config --global user.email "ci@users.noreply.github.com"
                git config --global user.name "CI Bot"

                git clone --branch gh-pages https://Zhang-XC:$GIT_TOKEN@github.com/Zhang-XC/test-automation.git gh-pages

                rm -rf gh-pages/*
                cp -r ./report/html/* gh-pages/

                cd gh-pages
                git add .
                git commit -m "Update Allure report from Jenkins" || echo "Nothing to commit"
                git push origin gh-pages
            '''
        }
    }

    stage('Cleanup') {
        sh 'pkill -u jenkins -x uv || true'
    }
}