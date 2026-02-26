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

        stage('Build') {
            steps {
                retry(3) {
                    sh 'docker compose build'
                }
        }

        stage('Run') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }
}
