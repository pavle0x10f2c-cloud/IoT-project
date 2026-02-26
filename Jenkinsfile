pipeline {
    agent any

    environment {
        DISPLAY = ':0'
    }

    stages {
        stage('Pull') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/pavle0x10f2c-cloud/IoT-project.git'
            }
        }

        stage('Setup') {
            steps {
                sh 'xhost +local:docker || true'
            }
        }

        stage('Build') {
            steps {
                retry(3) {
                    sh 'docker compose build'
                }
            }
        }

        stage('Run') {
            steps {
            withCredentials([file(credentialsId: 'iot-env', variable: 'ENV_FILE')]) {
                sh 'cp $ENV_FILE .env'
                sh 'docker compose up -d'
                }
            }
        }
    }
}
