void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/C0atRack/Django-Equipment-Management"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

pipeline {
    agent { label 'Alpine Python Container'}
    stages{
        stage('Clone repo'){
            steps{
                updateGitlabCommitStatus name: 'Clone repo', state: 'running'
                checkout scm
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Clone repo', state: 'success'
                }
                failure{
                    updateGitlabCommitStatus name: 'Clone repo', state: 'failed'
                }
            }
        }
        
        stage('Setup venv'){
            steps{
                updateGitlabCommitStatus name: 'Testing run', state: 'running'
                sh('echo Hello world!')
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Testing run', state: 'success'
                }
                failure{
                    updateGitlabCommitStatus name: 'Testing run', state: 'failed'
                }
            }
        }
    }
    post{
        success{
            setBuildStatus("Jenkins pipeline", "SUCCESS")
        }
        failure{
            setBuildStatus("Jenkins pipeline", "FAIL")
        }
    }
}
