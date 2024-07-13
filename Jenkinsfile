pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: slave
spec:
  containers:
  - name: helm
    image: 'alpine/helm:3.9.0'
    command:
    - cat
    tty: true
  - name: kubectl
    image: 'bitnami/kubectl:1.21.3'
    command:
    - cat
    tty: true
  - name: docker
    image: 'docker:latest'
    command:
    - cat
    tty: true
  - name: jnlp
    image: 'jenkins/inbound-agent:4.10-1'
    args: '${computer.jnlpmac} ${computer.name}'
            """
        }
    }
    environment {
        DOCKER_IMAGE = 'razasraf7/domyduda'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'RazAsraf7/FastAPI-App'
        GITHUB_TOKEN = credentials('github-credentials')
    }
    stages {
        stage("Checkout Code") {
            steps {
                checkout scm
            }
        }

        stage("Install Dependencies") {
            steps {
                container('helm') {
                    sh 'helm upgrade --install domyduda ./domyduda --namespace default'
                }
            }
        }

        stage("Build Docker Image") {
            steps {
                script {
                    container('docker') {
                        dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                    }
                }
            }
        }

        stage('Wait for Pods and Health Check') {
            steps {
                container('kubectl') {
                    script {
                        // Wait for the deployment to complete
                        sh 'kubectl rollout status deployment/domyduda --namespace default'

                        // Port forward the service to localhost
                        sh '''
                            kubectl port-forward svc/domyduda 8000:8000 --namespace default &
                            sleep 10
                        '''

                        // Check the application's health
                        def response = sh(script: "curl -s http://localhost:8000/health", returnStdout: true).trim()
                        if (response == 'OK') {
                            echo 'Health check passed.'
                        } else {
                            error('Health check failed.')
                        }
                    }
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    container('docker') {
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
                withCredentials([string(credentialsId: 'github-credentials', variable: 'GITHUB_TOKEN')]) {
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
        always {
            cleanWs()
        }
        success {
            script {
                if (env.BRANCH_NAME != 'main') {
                    echo 'Merge request created successfully.'
                } else {
                    echo 'Docker image pushed successfully.'
                }
            }
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
