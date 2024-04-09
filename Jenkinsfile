void setBuildStatus(String job_context, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/C0atRack/Django-Equipment-Management"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: job_context],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", state: state]] ]
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
                    setBuildStatus("Git Clone", "SUCCESS");
                }
                failure{
                    updateGitlabCommitStatus name: 'Clone repo', state: 'failed'
                    setBuildStatus("Git Clone", "FAIL");
                }
            }
        }
        
        stage('Setup venv'){
            steps{
                updateGitlabCommitStatus name: 'Setup Venv', state: 'running'
                sh('echo Hello world!')
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Setup Venv', state: 'success'
                    setBuildStatus("venv setup", "SUCCESS");
                }
                failure{
                    updateGitlabCommitStatus name: 'Setup Venv', state: 'failed'
                    setBuildStatus("venv setup", "FAIL");
                }
            }
        }
    }
}
