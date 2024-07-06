pipeline {
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: docker
                image: docker:20.10.8
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-sock
                  mountPath: /var/run/docker.sock
              volumes:
              - name: docker-sock
                hostPath:
                  path: /var/run/docker.sock
            """
        }
    }
    environment {
        USERNAME = 'root'
        ROOT_PASSWORD = '212928139'
        HOST = 'mongodb'
        PORT = '27017'
        MONGO_URI = "mongodb://USERNAME:ROOT_PASSWORD@HOST:PORT/"
    }
    stages {
        stage('Pull Docker Image') {
            steps {
                container('docker') {
                    script {
                        sh 'docker pull razasraf7/domyduda'
                    }
                }
            }
        }
        stage('Run Application') {
            steps {
                container('docker') {
                    script {
                        sh '''
                        docker run -d --name my_app_container \
                        -e MONGO_URI=$MONGO_URI \
                        razasraf7/domyduda
                        '''
                    }
                }
            }
        }
        stage('Check Application') {
            steps {
                container('docker') {
                    script {
                        // Replace this with your application's health check or test command
                        sh '''
                        # Wait for a few seconds to ensure the application is up
                        sleep 10
                        # Check if the application is running correctly
                        docker exec my_app_container curl -f http://localhost:8000/ || exit 1
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            container('docker') {
                script {
                    sh 'docker stop my_app_container'
                    sh 'docker rm my_app_container'
                }
            }
        }
    }
}
