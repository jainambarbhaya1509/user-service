pipeline {
    agent any

    environment {
        IMAGE_NAME = "jainambarbhaya15/user-service"
        IMAGE_TAG = "${BUILD_NUMBER}"

        GITOPS_REPO = "https://github.com/jainambarbhaya1509/gitops.git"
        GIT_BRANCH = "main"
    }

    stages {

        stage('Checkout App Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'jainambarbhaya15',
                        passwordVariable: 'jainamb1509'
                    )
                ]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Clone GitOps Repo') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'jainambarbhaya1509',
                        passwordVariable: 'jainamb1509'
                    )
                ]) {

                    sh '''
                    rm -rf gitops

                    git clone https://$GIT_USER:$GIT_TOKEN@github.com/jainambarbhaya1509/gitops.git gitops
                    '''
                }
            }
        }

        stage('Update Helm Chart') {
            steps {

                sh """
                    sed -i 's/tag:.*/tag: "${IMAGE_TAG}"/' \
                    gitops/helm/user-service/values.yaml

                    cat gitops/helm/user-service/values.yaml
                """
            }
        }

        stage('Commit & Push Changes') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'jainambarbhaya1509',
                        passwordVariable: 'jainamb1509'
                    )
                ]) {

                    sh '''
                    cd gitops

                    git config user.email "jainambarbhaya1509@gmail.com"
                    git config user.name "jainambarbhaya1509"

                    git add .

                    git commit -m "Update image tag to ${IMAGE_TAG}" || true

                    git push origin main
                    '''
                }
            }
        }
    }

    post {

        success {
            echo "Docker image pushed successfully"
            echo "Helm chart updated"
            echo "ArgoCD will sync automatically"
        }

        failure {
            echo "Pipeline failed"
        }
    }
}