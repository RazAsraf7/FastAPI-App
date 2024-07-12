pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: helm
    image: alpine/helm:3.9.0
    command:
    - cat
    tty: true
  - name: kubectl
    image: bitnami/kubectl:1.21.3
    command:
    - cat
    tty: true
"""
        }
    }
    environment {
        DOCKER_IMAGE = "razasraf7/domyduda"
        GITHUB_REPO = "RazAsraf7/FastAPI-App"
        GITHUB_TOKEN = credentials('github_credentials')
        GITHUB_API_URL = "https://api.github.com"
        DOCKERHUB_CREDENTIALS = credentials('docker_credentials')
    }
    stages {
        stage('Package and Deploy Application') {
            steps {
                container('helm') {
                    script {
                        sh '''
                        cd domyduda
                        # Deploy the Helm chart
                        helm dependency update
                        cd ..
                        helm install my-app ./domyduda
                        '''
                    }
                }
            }
        }
        stage('Port Forward and Health Check') {
            steps {
                container('kubectl') {
                    script {
                        // Start port forwarding in the background
                        sh "kubectl port-forward svc/domyduda 8000:8000 &"

                        // Give port-forward some time to establish
                        sleep 5

                        // Check health endpoint
                        def healthCheckResponse = sh(script: "curl -s http://localhost:8000/health", returnStdout: true).trim()
                        if (healthCheckResponse == 'OK') {
                            echo 'Health check passed!'
                        } else {
                            error 'Health check failed!'
                        }

                        // Optionally, you may want to kill the port-forward process after the check
                        sh "pkill -f 'kubectl port-forward svc/domyduda 8000:8000'"
                }
            }
        }
    }
    post {
        always {
            container('helm') {
                script {
                    sh '''
                    # Uninstall the application and MongoDB
                    helm uninstall my-app || true
                    '''
                }
            }
        }
    }
}
