pipeline {
    agent any

    environment {
        IMAGE_NAME = "jainambarbhaya/user-service"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'jainambarbhaya',
                        passwordVariable: 'jainamb1509'
                    )
                ]) {
                    sh '''
                    echo $DOCKER_PASS | docker login \
                    -u $DOCKER_USER \
                    --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Update GitOps Repo') {
            steps {
                sshagent(['github-ssh']) {

                    sh '''
                    rm -rf gitops

                    git clone \
                    git@github.com:jainambarbhaya1509/gitops.git

                    cd gitops

                    sed -i.bak \
                    "s/tag:.*/tag: ${IMAGE_TAG}/" \
                    environments/dev/user-service-values.yaml

                    rm -f environments/dev/user-service-values.yaml.bak

                    git config user.email "jainambarbhaya1509@gmail.com"

                    git config user.name "jainambarbhaya1509"

                    git add .

                    git commit -m "Deploy image ${IMAGE_TAG}" || true

                    git push origin main
                    '''
                }
            }
        }
    }
}