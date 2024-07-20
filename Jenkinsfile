pipeline {
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: helm-kubectl
                image: razasraf7/helm_and_kubectl
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              - name: docker
                image: docker:19.03.12
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              - name: python
                image: python:3.9
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              volumes:
              - name: docker-socket
                hostPath:
                  path: /var/run/docker.sock
            """
        }
    }
    environment {
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'RazAsraf7/FastAPI-App'
        EMAIL_RECIPIENTS = 'razasraf7@gmail.com'
    }
    stages {
        stage('Build Helm Chart') {
            steps {
                container('helm-kubectl') {
                    sh '''
                    cd domyduda
                    helm dependency update
                    cd ..
                    helm upgrade --install domyduda ./domyduda
                    '''
                }
            }
        }
        stage('Check if Application Works') {
            steps {
                container('helm-kubectl') {
                    sh '''
                    sleep 5
                    kubectl port-forward svc/domyduda 8000:8000 &
                    sleep 5
                    curl -s http://localhost:8000/health
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                container('python') {
                    script {
                        // Run tests
                        sh 'pip install -r requirements.txt'
                        sh 'pytest tests'
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        dockerImage = docker.build("razasraf7/domyduda:latest", "--no-cache .")
                    }
                }
            }
        }
        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                container('docker') {
                    script {
                        docker.withRegistry('https://registry.hub.docker.com', 'docker_credentials') {
                            dockerImage.push("latest")
                        }
                    }
                }
            }
        }
        stage('Create Merge Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github_token', variable: 'GITHUB_TOKEN')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into main"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                        sh """
                            curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "main" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Build succeeded.'
        }
        failure {
            emailext(
                to: "${EMAIL_RECIPIENTS}",
                subject: "Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """\
                <p>Dear User,</p>
                <p>The Jenkins build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> has failed.</p>
                <p>Check the details at: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                <p>Best Regards,<br/>Jenkins</p>
                """,
                mimeType: 'text/html'
            )
        }
    }
}
