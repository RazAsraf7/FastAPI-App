pipeline {
    agent {
        kubernetes {
            defaultContainer 'domyduda-ffb7fd-bxqsw'
        }
    }
    environment {
        DOCKER_CREDS = credentials('docker_credentials')
        GITHUB_CREDS = credentials('github_credentials')
        DOCKER_REPOSITORY = 'razasraf7/domyduda'
        GITHUB_REPOSITORY = 'FastAPI-App'
    }
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }
    }
}   