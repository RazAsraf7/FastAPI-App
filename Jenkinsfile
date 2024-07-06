pipeline {
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: helm
                image: alpine/helm:3.5.4
                command:
                - cat
                tty: true
              - name: kubectl
                image: bitnami/kubectl:1.20
                command:
                - cat
                tty: true
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
        stage('Deploy MongoDB') {
            steps {
                container('helm') {
                    script {
                        sh '''
                        # Add the Bitnami repository and update
                        helm repo add bitnami https://charts.bitnami.com/bitnami
                        helm repo update

                        # Install MongoDB using the custom values file
                        helm install my-mongodb bitnami/mongodb -f mongodb-architecture.yaml
                        '''
                    }
                }
            }
        }
        stage('Package and Deploy Application') {
            steps {
                container('helm') {
                    script {
                        sh '''
                        # Navigate to the directory containing the Helm chart
                        cd domyduda

                        # Package the Helm chart
                        helm package .

                        # Deploy the Helm chart
                        helm install my-app ./domyduda-0.1.0.tgz --set mongodb.uri=$MONGO_URI
                        '''
                    }
                }
            }
        }
        stage('Check Application') {
            steps {
                container('kubectl') {
                    script {
                        // Replace this with your application's health check or test command
                        sh '''
                        # Wait for a few seconds to ensure the application is up
                        sleep 30
                        # Check if the application is running correctly
                        kubectl run -i --rm --tty busybox --image=busybox --restart=Never -- curl -f http://my-app.default.svc.cluster.local:8000/ || exit 1
                        '''
                    }
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
                    helm uninstall my-app
                    helm uninstall my-mongodb
                    '''
                }
            }
        }
    }
}
