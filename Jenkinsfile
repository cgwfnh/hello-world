pipeline {
  agent any
  stages {
    stage('Source') {
      steps {
        git 'https://github.com/cgwfnh/hello-world.git'
      }
    }
  }
  environment {
    COMPLETED_MSG = 'Build done!'
  }
}