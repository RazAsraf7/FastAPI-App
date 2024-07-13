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
        RELEASE_NAME = 'domyduda'
        CHART_NAME = 'domyduda'
        DOCKER_IMAGE = 'razasraf7/domyduda'
        NAMESPACE = 'default'
        HELM_VALUES = 'values.yaml' // Use if you have a values file
        BRANCH_NAME = env.BRANCH_NAME
    }
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Helm Lint') {
            steps {
                container('helm') {
                    sh 'helm lint $CHART_NAME'
                }
            }
        }
        stage('Helm Dependencies Update') {
            steps {
                container('helm') {
                    sh 'helm dependency update $CHART_NAME'
                }
            }
        }
        stage('Helm Install/Upgrade') {
            steps {
                container('helm') {
                    sh '''
                        helm upgrade --install $RELEASE_NAME ./$CHART_NAME \
                        --set image.repository=$DOCKER_IMAGE \
                        --namespace $NAMESPACE
                    '''
                }
            }
        }
        stage('Wait for Pods') {
            steps {
                container('kubectl') {
                    sh 'kubectl rollout status deployment/$RELEASE_NAME --namespace $NAMESPACE'
                }
            }
        }
        stage('Port Forward and Health Check') {
            steps {
                container('kubectl') {
                    script {
                        sh '''
                            kubectl port-forward svc/$RELEASE_NAME 8000:8000 --namespace $NAMESPACE &
                            sleep 10
                        '''
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
        stage('Conditional Actions') {
            steps {
                script {
                    if (BRANCH_NAME != 'main') {
                        // Create merge request to main
                        echo 'Creating merge request to main'
                        sh '''
                            curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{"title":"Merge branch '${BRANCH_NAME}' into main","head":"'${BRANCH_NAME}'","base":"main"}' \
                            https://api.github.com/repos/${GITHUB_REPO}/pulls
                        '''
                    } else {
                        // Push to Docker Hub
                        container('docker') {
                            withCredentials([usernamePassword(credentialsId: 'docker_credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                                sh '''
                                    docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                                    docker build -t $DOCKER_IMAGE .
                                    docker push $DOCKER_IMAGE
                                '''
                            }
                        }
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
                if (BRANCH_NAME != 'main') {
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
