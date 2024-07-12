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
  - name: curl
    image: 'curlimages/curl:7.87.0'
    command:
    - cat
    tty: true
  - name: jnlp
    image: 'jenkins/inbound-agent:4.10-1'
    args:
    - \$(JENKINS_SECRET)
    - \$(JENKINS_NAME)
            """
        }
    }
    environment {
        GIT_CREDENTIALS_ID = 'github_credentials' // Replace with your actual credentials ID
    }
    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/RazAsraf7/FastAPI-App',
                            credentialsId: env.GIT_CREDENTIALS_ID
                        ]]
                    ])
                }
            }
        }
        stage('Helm Lint') {
            steps {
                container('helm') {
                    sh 'helm lint ./domyduda'
                }
            }
        }
        stage('Helm Package') {
            steps {
                container('helm') {
                    sh 'helm package ./domyduda'
                }
            }
        }
        stage('Helm Deploy') {
            steps {
                container('kubectl') {
                    sh 'helm upgrade --install domyduda ./domyduda'
                }
            }
        }
        stage('Port Forward and Health Check') {
            steps {
                container('kubectl') {
                    script {
                        def portForwardCmd = "kubectl port-forward svc/domyduda 8000:8000 &"
                        sh portForwardCmd
                        sleep 10 // wait for port-forwarding to establish
                    }
                }
                container('curl') {
                    script {
                        def healthCheckCmd = "curl http://localhost:8000/health"
                        def response = sh(script: healthCheckCmd, returnStdout: true).trim()
                        if (response != 'healthy') {
                            error "Health check failed: ${response}"
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            container('kubectl') {
                script {
                    // Clean up resources
                    sh 'helm uninstall domyduda || true'
                }
            }
        }
    }
}
