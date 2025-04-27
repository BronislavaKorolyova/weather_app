pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        DOCKER_IMAGE = 'yourdockerhubusername/yourappname'
        SLACK_CHANNEL = '#jenkins-alerts'
        SLACK_TOKEN = credentials('global-slack')
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        SSH_CREDENTIALS = 'ssh-ec2-credentials-id'  // SSH key stored in Jenkins credentials
        EC2_HOST = 'your-ec2-public-ip'             // e.g., 13.48.22.11
        DEPLOY_DIR = '/home/ec2-user/yourapp'        // Path where you run docker-compose/docker run
    }

    stages {
        stage('Workspace Clean Before Build') {
            steps {
                cleanWs()
            }
        }

        stage('Run Pylint') {
            steps {
                echo 'Running Pylint'
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh 'pylint **/*.py'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                pytest test/ --junitxml=test-reports/report.xml
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'test-reports/report.xml'
                archiveArtifacts artifacts: 'test-reports/report.xml', fingerprint: true
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Inspect Docker Image') {
            steps {
                sh '''
                echo "Docker Image History:"
                docker history ${DOCKER_IMAGE}:${BUILD_NUMBER}

                echo "Docker Image Details:"
                docker inspect ${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                withDockerRegistry(credentialsId: "${DOCKERHUB_CREDENTIALS}", url: '') {
                    sh '''
                    echo "Pushing Build Number Tag..."
                    docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}

                    echo "Tagging Image as Latest..."
                    docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest

                    echo "Pushing Latest Tag..."
                    docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Docker Cleanup After Build') {
            steps {
                sh '''
                echo "Pruning unused Docker objects..."
                docker system prune -af
                '''
            }
        }

        stage('Deploy to EC2 and Restart App') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS}"]) {
                    sh '''
                    echo "Connecting to EC2 instance and deploying new version..."
                    ssh -o StrictHostKeyChecking=no ec2-user@${EC2_HOST} '
                        docker pull ${DOCKER_IMAGE}:latest &&
                        docker stop flask-app || true &&
                        docker rm flask-app || true &&
                        docker run -d --name flask-app -p 80:5000 ${DOCKER_IMAGE}:latest
                    '
                    '''
                }
            }
        }
    }

    post {
        success {
            slackSend(channel: "${env.SLACK_CHANNEL}", color: 'good',
                      message: "🎉 SUCCESS: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER} completed and deployed!",
                      tokenCredentialId: "${env.SLACK_TOKEN}")
        }
        failure {
            slackSend(channel: "${env.SLACK_CHANNEL}", color: 'danger',
                      message: "❌ FAILURE: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER} failed!",
                      tokenCredentialId: "${env.SLACK_TOKEN}")
        }
        always {
            slackSend(channel: "${env.SLACK_CHANNEL}", color: '#439FE0',
                      message: "ℹ️ Pipeline completed: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                      tokenCredentialId: "${env.SLACK_TOKEN}")
            cleanWs()
        }
    }
}
